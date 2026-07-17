from datetime import datetime

from disnake import Embed

from utils.api_wrapper.models import Planet
from utils.dataclasses import Factions
from utils.mixins import EmbedReprMixin


class RegionEmbed(Embed, EmbedReprMixin):
    def __init__(
        self,
        planet: Planet,
        lang_code: str,
        container_json: dict,
    ):
        super().__init__()
        now_seconds = int(datetime.now().timestamp())
        for region in sorted(planet.regions.values(), key=lambda x: x.size):
            text_display = []
            if (
                planet.homeworld
                and not region.is_available
                and any(
                    [r for r in planet.regions.values() if r.size > region.size]
                )
            ):
                text_display = [f"~~", "".join(text_display), "~~"]
            if region.flags == 1 and planet.faction == Factions.automaton:
                text_display.append(
                    f"\n-# {region.emoji} Class {region.size} Megafactory"
                )
            else:
                text_display.append(f"\n-# {region.emoji} {region.type.name.replace('_', ' ').title()}")
            if region.description and len(planet.regions) < 5:
                text_display.append(f"\n-# {region.descriptions[lang_code]}")
            if region.is_available:
                text_display.append(f"\n-# {container_json['heroes']}: **{region.players}** ({region.players / planet.stats.player_count:.2%})")
                health_to_get_from = (
                    planet.max_health
                    if not planet.event
                    else planet.event.max_health
                )
                text_display.append(f"\n{container_json['boost_when_liberated']}: **{(region.max_health * region.damage_multiplier) / health_to_get_from:.2%}**")
                if (
                    region.tracker
                    and region.tracker.change_rate_per_hour > 0
                    and (
                    planet.tracker
                    and planet.tracker.change_rate_per_hour > 0
                    and (
                        region.tracker.complete_time
                        < planet.tracker.complete_time
                    )
                )
                ):
                    percent_at = planet.tracker.percentage_at(
                        region.tracker.complete_time
                    )
                    percent_total = percent_at + (
                            (region.max_health * region.damage_multiplier)
                            / health_to_get_from
                    )
                    text_display.append(f"\n-# *from **{percent_at:.2%}** to **{percent_total:.2%}** at time of liberation!*")
                text_display.append(f"\n{region.health_bar}")
                text_display.append(f"\n`{region.perc:^25,.2%}`")
                if region.tracker and region.tracker.change_rate_per_hour > 0:
                    change = f"{region.tracker.change_rate_per_hour:.2%}/hr"
                    text_display.append(
                        f"\n`{change:^25}`"
                        + f"\n-# {container_json['liberated']} <t:{int(region.tracker.complete_time.timestamp())}:R>"
                    )
            elif region.owner.full_name != "Humans":
                stat_to_use = (
                    container_json["liberation"]
                    if not planet.event
                    else container_json["defence_duration"]
                )
                if region.availability_factor != 1 and (
                        region.availability_factor) > (
                    planet.event.progress
                    if planet.event
                    else 1 - planet.health_perc
                ):
                    text_display.append(container_json["unlocked_when"].format(
                        stat_to_use=stat_to_use,
                        av_factor=f"{region.availability_factor:.0%}",
                    ))
                if planet.event:
                    current_percentage = (
                        now_seconds - planet.event.start_time_datetime.timestamp()
                    ) / (
                        planet.event.end_time_datetime.timestamp()
                        - planet.event.start_time_datetime.timestamp()
                    )
                    region_avail_timestamp = int(
                        now_seconds
                        + (
                            (
                            (region.availability_factor - current_percentage)
                            / (1 - current_percentage)
                            )
                                * (
                                planet.event.end_time_datetime.timestamp()
                                - now_seconds
                                )
                        )
                    )
                    text_display.append(f"\n-# <t:{region_avail_timestamp}:R>")
            for text in text_display:
                self.add_field(f"{region.owner.emoji} **{region.names.get(lang_code, region.name)}**", text)