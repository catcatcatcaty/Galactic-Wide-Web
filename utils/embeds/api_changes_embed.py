from disnake import Embed

from utils.api_wrapper.models import Planet
from utils.containers.api_changes import STATUS_DICT
from utils.dataclasses import APIChanges
from utils.embeds.galactic_war_effect_embed import galactic_war_effect_embed
from utils.emojis import Emojis
from utils.mixins import EmbedReprMixin


class api_changes_embed(Embed, EmbedReprMixin):
    def __init__(
        self, api_changes: list[APIChanges], planets: dict[int, Planet]):
        super().__init__(
        )

        for api_change in api_changes:
            if api_change.stat_source not in [
                "Global Resources",
                "Galactic War Effects",
                "Task",
                "Personal Order",
            ]:
                old_stat = getattr(api_change.old_object, api_change.property)
                new_stat = getattr(api_change.new_object, api_change.property)
            match api_change.stat_source:
                case "Global Resources":
                    self.add_field(f"CHANGES TO GLOBAL RESOURCES",
                                   f"Before:\n```py\n{api_change.old_object}```\n\nAfter:\n```py\n{api_change.new_object}```")
                case "Galactic War Effects":
                    content = ""
                    if effects_removed := [
                        gwe
                        for id, gwe in api_change.old_object.items()
                        if id not in api_change.new_object
                    ]:
                        content += "\n### Galactic Effect(s) Removed ❌"
                        for gwe in effects_removed:
                            gwe_container = galactic_war_effect_embed(gwe, [], False, False)
                            gwe_content = (
                                "\n"
                                + gwe_container.fields[0].name
                                + gwe_container.fields[1].value
                                + "\n"
                            )
                            content += gwe_content

                    if effects_added := [
                        gwe
                        for id, gwe in api_change.new_object.items()
                        if id not in api_change.old_object
                    ]:
                        content += "\n### Galactic Effect(s) Added :white_check_mark:"
                        for gwe in effects_added:
                            gwe_container = galactic_war_effect_embed(gwe, [], False, False)
                            gwe_content = (
                                "\n"
                                + gwe_container.fields[0].name
                                + gwe_container.fields[1].value
                                + "\n"
                            )
                            content += gwe_content

                    if effects_removed or effects_added:
                        self.add_field("-", content)
                case "Task":
                    self.add_field(f"Update to **{api_change.stat_name}**",
                                       f"Target for task **#{api_change.property}**\n        **{api_change.old_object.target:,} {Emojis.Stratagems.right} {api_change.new_object.target:,}**")
                case "Personal Order":
                    self.add_field(f"Personal Order has changed",
                                   f"**{api_change.old_object.id}** {Emojis.Stratagems.right} **{api_change.new_object.id}**")
                case "Planet":
                    if not next(
                        (
                            s
                            for s in self.fields
                            if api_change.new_object.names.get(
                                "en-GB", api_change.new_object.name
                            )
                            in s.value
                        ),
                        None,
                    ):
                        self.add_field(f"Update to **{api_change.new_object.names.get('en-GB', api_change.new_object.name)}**",
                                       f"{api_change.new_object.faction.emoji}{api_change.new_object.exclamations}")
                    match api_change.property:
                        case "position":
                            self.add_field(
                                f"Planet has __**moved**__",
                                f"\n**{old_stat['x']}, {old_stat['y']}**"
                                      f"\n                         {Emojis.Stratagems.down}"
                                      f"\n**{new_stat['x']}, {new_stat['y']}**"
                                      f"\n**({(new_stat['x'] - (old_stat['x'])):+.8f}, {(new_stat['y'] - (old_stat['y'])):+.8f})**"
                                )
                        case "waypoints":
                            content = ""
                            if waypoints_removed := list(set(old_stat) - set(new_stat)):
                                for wp in waypoints_removed:
                                    planet = planets.get(wp)
                                    if planet:
                                        content += f"\n-# - **{planet.names.get('en-GB', planet.name)}**"
                                    else:
                                        content += f"\n-# - **UNKNOWN PLANET**"
                            if waypoints_added := list(set(new_stat) - set(old_stat)):
                                content += "\n### Waypoint(s) Added :white_check_mark:"
                                for wp in waypoints_added:
                                    planet = planets.get(wp)
                                    if planet:
                                        content += f"\n-# - **{planet.names.get('en-GB', planet.name)}**"
                                    else:
                                        content += f"\n-# - **UNKNOWN PLANET**"
                            if waypoints_added or waypoints_removed:
                                self.add_field("Waypoint(s) Removed ❌", content)
                        case "max_health":
                            self.add_field("**Max health** has changed",
                                           f"from:\n**{old_stat:,}** {Emojis.Stratagems.right} **{new_stat:,}** | {(new_stat - old_stat):+,}")
                        case "faction":
                            self.add_field(f"**Owner** has changed",
                                           f"from:\n{old_stat.emoji} **{old_stat.full_name}** {Emojis.Stratagems.right} **{new_stat.full_name}** {new_stat.emoji}")
                        case "regen_perc_per_hour":
                            self.add_field(f"**Regen** has changed",
                                           f"from:\n**{old_stat:+.2%}**/hr {Emojis.Stratagems.right} **{new_stat:+.2%}**/hr")
                        case "dss_in_orbit":
                            if new_stat == True:
                                self.add_field("DSS is **now in orbit** :white_check_mark:", "-")
                            else:
                                self.add_field("DSS is **no longer in orbit** ❌", "-")
                        case "active_effects":
                            if effects_removed := [
                                gwe for gwe in old_stat if gwe not in new_stat
                            ]:
                                text_display = ""
                                for effect in effects_removed:
                                    gwe_container = galactic_war_effect_embed(
                                        effect, [], False, False
                                    )
                                    gwe_content = (
                                        "\n"
                                        + gwe_container.fields[0].name
                                        + gwe_container.fields[1].value
                                        + "\n"
                                    )
                                    text_display += gwe_content
                                self.add_field( f"Effect(s) __removed__ ❌", text_display)

                            if effects_added := [
                                gwe for gwe in new_stat if gwe not in old_stat
                            ]:
                                text_display = ""
                                for effect in effects_added:
                                    gwe_container = galactic_war_effect_embed(
                                        effect, [], False, False
                                    )
                                    gwe_content = (
                                        "\n"
                                        + gwe_container.fields[0].name
                                        + gwe_container.fields[1].value
                                        + "\n"
                                    )
                                    text_display += gwe_content
                                self.add_field(f"Effect(s) __added__ :white_check_mark:", text_display)
                        case "sector":
                            self.add_field(f"__**Sector has changed__:", f"**{old_stat}** {Emojis.Stratagems.right} **{new_stat}**")
                        case _:
                            self.add_field(f"**{api_change.stat_name}** has changed from:\n**{old_stat}** {Emojis.Stratagems.right} **{new_stat}**", "")
                case "Region":
                    if not next(
                        (
                            s
                            for s in self.fields
                            if api_change.new_object.name
                            in s.value
                        ),
                        None,
                    ):
                        self.add_field(f"Update for {api_change.new_object.emoji} {api_change.new_object.type.name.replace('_', ' ').title()}",
                                       f"{api_change.new_object.name} on {api_change.new_object.planet.names.get('en-GB', api_change.new_object.planet.name)}{api_change.new_object.planet.faction.emoji}{api_change.new_object.planet.exclamations}")
                    match api_change.property:
                        case "owner":
                            self.add_field(f"**Owner** has changed from:",
                                           f"{old_stat.emoji} **{old_stat.full_name}** {Emojis.Stratagems.right} **{new_stat.full_name}** {new_stat.emoji}")
                        case "max_health":
                            self.add_field(f"**Max health** has changed from:",
                                           f"**{old_stat:,}** {Emojis.Stratagems.right} **{new_stat:,}** | {(new_stat - old_stat):+,}")
                        case "regen_perc_per_hour":
                            self.add_field(f"**Regen** has changed from:",
                                           f"**{old_stat:+.2%}**/hr {Emojis.Stratagems.right} **{new_stat:+.2%}**/hr")
                        case "is_available":
                            if new_stat == True:
                                self.add_field(f"Is **now available** :white_check_mark:", "-")
                            else:
                                self.add_field(f"Is **no longer available** ❌", "-")
                        case "damage_multiplier":
                            self.add_field( f"Damage multiplier has changed from:",
                                           f"**{old_stat}x** {Emojis.Stratagems.right} **{new_stat}x**")
                        case _:
                            self.add_field( f"{api_change.stat_name} has changed from:",
                                           f"**{old_stat}** {Emojis.Stratagems.right} **{new_stat}**")
                case "Episode":
                    if not next(
                        (
                            c
                            for c in self.fields
                            if str(api_change.new_object.id) in c.value
                        ),
                        None,
                    ):
                        self.add_field(f"Update to Episode **{api_change.new_object.id}**", "-")
                    match api_change.property:
                        case "faction":
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{old_stat.emoji} {old_stat.full_name}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{new_stat.emoji} {new_stat.full_name}")
                        case "status":
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{STATUS_DICT.get(old_stat, 'UNKNOWN')}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{STATUS_DICT.get(new_stat, 'UNKNOWN')}")
                        case "phases":
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{[f'{p.id} - {p.intro_title}' for p in old_stat]}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{[f'{p.id} - {p.intro_title}' for p in new_stat]}")
                        case "rewards":
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{[f'{r.amount} x {r.item_name}' for r in old_stat]}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{[f'{r.amount} x {r.item_name}' for r in new_stat]}")
                        case _:
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{old_stat}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{new_stat}")
                case "Phase":
                    if not next(
                        (
                            c
                            for c in self.fields
                            if str(api_change.new_object.id) in c.value
                        ),
                        None,
                    ):
                        self.add_field( f"Update to Phase **{api_change.new_object.id}**", "-")
                    match api_change.property:
                        case "status":
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{STATUS_DICT.get(old_stat, 'UNKNOWN')}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{STATUS_DICT.get(new_stat, 'UNKNOWN')}")
                        case "rewards":
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{[f'{r.amount} x {r.item_name}' for r in old_stat]}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{[f'{r.amount} x {r.item_name}' for r in new_stat]}")
                        case _:
                            self.add_field(f"**{api_change.stat_name}** has changed from:",
                              f"{old_stat}"
                                    f"\n{Emojis.Stratagems.down}"
                                    f"\n{new_stat}")
