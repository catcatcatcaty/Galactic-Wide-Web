from data.lists import CUSTOM_COLOURS
from datetime import datetime, timedelta, timezone
from disnake import Colour, Embed
from utils.api_wrapper.models import DSS, Campaign
from utils.emojis import Emojis
from utils.functions import health_bar
from utils.mixins import EmbedReprMixin
from utils.trackers import BaseTrackerEntry

STATUSES = {
    0: "inactive",
    1: "preparing",
    2: "active",
    3: "on_cooldown",
}


class DSSEmbed(Embed, EmbedReprMixin):
    def __init__(
        self,
        language_json: dict,
        dss_data: DSS,
        next_vote_campaigns: list[Campaign],
    ):
        super().__init__(
            title=language_json["embeds"]["DSSEmbed"]["title"],
            colour=Colour.from_rgb(*CUSTOM_COLOURS["DSS"]),
        )
        if (
            not dss_data
            or dss_data.flags in [0, 2]
            or (
                all([ta.status == 0 for ta in dss_data.tactical_actions])
                and dss_data.move_timer_datetime
                > datetime.now(tz=timezone.utc) + timedelta(days=30)
            )
        ):
            self.add_field("The DSS is currently unavailable.", "")
            self.colour = Colour.brand_red()
            return
        self.description = language_json["embeds"]["DSSEmbed"]["stationed_at"].format(
            planet=dss_data.planet.names.get(
                language_json["code_long"], dss_data.planet.name
            ),
            faction_emoji=getattr(
                Emojis.Factions, dss_data.planet.faction.full_name.lower()
            ),
        )
        self.description += language_json["embeds"]["DSSEmbed"]["next_move"].format(
            timestamp=f"<t:{int(dss_data.move_timer_datetime.timestamp())}:R>"
        )
        self.set_thumbnail(
            "https://fluxerusercontent.com/attachments/1476525402340249794/1530880774960582656/1000108518.png"
        ).set_image(
            "https://fluxerusercontent.com/attachments/1476525402340249794/1530881335462199296/1000108519.jpg"
        )
        for tactical_action in dss_data.tactical_actions:
            tactical_action: DSS.TacticalAction
            status = STATUSES[tactical_action.status]
            if status == "preparing":
                cost = ""
                for ta_cost in tactical_action.cost:
                    ta_cost_change: BaseTrackerEntry = tactical_action.cost_changes[
                        ta_cost.item
                    ]
                    change_text = ""
                    if ta_cost_change and ta_cost_change.change_rate_per_hour != 0:
                        change = f"{ta_cost_change.change_rate_per_hour:+.2%}/hr"
                        change_text = f"\n`{change:^25}`"
                        change_text += f"\n-# {language_json['embeds']['Dashboard']['DSSEmbed']['active']} <t:{int(datetime.now(tz=timezone.utc).timestamp() + ta_cost_change.seconds_until_complete)}:R>"
                        ta_cost_health_bar = health_bar(
                            ta_cost.progress,
                            "MO" if ta_cost.progress != 1 else "Humans",
                            anim=True,
                            increasing=ta_cost_change.change_rate_per_hour > 0,
                        )
                    else:
                        ta_cost_health_bar = health_bar(
                            ta_cost.progress,
                            "MO" if ta_cost.progress != 1 else "Humans",
                        )
                    cost = (
                        f"{ta_cost_health_bar}\n"
                        f"`{ta_cost.progress:^25.2%}`"
                        f"{change_text}"
                    )
            elif status == "active":
                cost = f"{language_json['embeds']['DSSEmbed']['on_cooldown'].capitalize()} <t:{int(tactical_action.status_end_datetime.timestamp())}:R>"
            elif status == "on_cooldown":
                cost = f"{language_json['embeds']['DSSEmbed']['preparing'].capitalize()} <t:{int(tactical_action.status_end_datetime.timestamp())}:R>"
            else:
                continue
            localized_ta = language_json["embeds"]["DSSEmbed"]["tactical_actions"].get(
                tactical_action.name,
                {
                    "name": tactical_action.name,
                    "description": tactical_action.description,
                },
            )
            self.add_field(
                f"{tactical_action.emoji} {localized_ta['name']}",
                (
                    f"{language_json['embeds']['DSSEmbed']['status']}: **{language_json['embeds']['DSSEmbed'][status].capitalize()}**"
                    f"\n{localized_ta['description']}"
                    f"\n{cost}\n\u200b\n"
                ),
                inline=False,
            )
        if dss_data.votes:
            votes_text = "Current Votes:"
            for index, planet_votes_dict in enumerate(
                sorted(
                    dss_data.votes.available_planets,
                    key=lambda x: x[1],
                    reverse=True,
                ),
                start=1,
            ):
                if planet_votes_dict[1] == 0:
                    votes = 0.0
                else:
                    votes = planet_votes_dict[1] / dss_data.votes.total_votes
                votes_text += f"\n-# #{index} - {planet_votes_dict[0].faction.emoji} {planet_votes_dict[0].names.get(language_json['code_long'], planet_votes_dict[0].name)} - ({votes:.0%})"
            self.add_field("", votes_text, inline=False)

            predicted_field_value = ""
            for i, c in enumerate(next_vote_campaigns, start=1):
                predicted_field_value += f"\n-# #{i} - {c.faction.emoji} {c.planet.names.get(language_json['code_long'], c.planet.name)} - {c.planet.stats.player_count:,} Heroes"
            self.add_field(
                "Predicted next voting period", predicted_field_value, inline=False
            )
        else:
            self.add_field(
                "DSS voting data is unavailable.",
                "\n-# Apologies for the inconvenience",
                inline=False,
            )
