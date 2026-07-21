from disnake import Embed, Colour, Color

from utils.api_wrapper.models import Planet
from utils.dataclasses import PlanetFeatures, Factions
from utils.functions import get_end_time, short_format
from utils.mixins import EmbedReprMixin


class PlanetEmbed(Embed, EmbedReprMixin):
    def __init__(
        self,
        planet: Planet,
        lang_code: str,
        containers_json: dict,
        faction_json: dict,
        gambit_planets: dict[int, Planet],
    ):
        super().__init__(
        )
        self.add_planet_info(
            planet=planet,
            component_json=containers_json["planet_info"],
            factions_json=faction_json,
            gambit_planets=gambit_planets,
            lang_code=lang_code,
        )
        self.add_hero_stats(
            planet=planet,
            component_json=containers_json["hero_stats"]
        )
        self.add_misc_stats(
            planet=planet,
            component_json=containers_json["misc_stats"],
            faction_json=faction_json
        )
        self.set_default_colour(Colour.from_rgb(
                    *(
                        planet.faction.colour
                        if not planet.event
                        else planet.event.faction.colour
                    ),
        ))

    def add_planet_info(
        self,
        planet: Planet,
        component_json: dict,
        factions_json: dict,
        gambit_planets,
        lang_code: str,
    ):
        if planet.faction:
            description = "\n-# " + planet.description if planet.description else ""
            self.add_field(f"{planet.faction.emoji} {planet.names.get(lang_code, planet.name)}, {planet.exclamations}",
              f"\n{component_json['sector']}: **{planet.sector}**"
            + f"\n{component_json['owner']}: **{factions_json[planet.faction.full_name]}**{planet.faction.emoji}"
            + f"\n{description}"
            + f"\n")

            #EFFECTS
            effects_text = f""
            for pf in planet.planet_features:
                effects_text += f"\n-# {pf.emoji} {pf.name}"
            if effects_text != "":
                self.add_field(f"Features:", effects_text + f"\n")

            #SUBFACTIONS
            sf_text = f""
            for sf in planet.subfactions:
                sf_text += f"\n-# {sf.emoji} {sf.eng_name}"
            if sf_text != "":
                self.add_field(f"Subfactions:", effects_text + f"\n")

            #COMMUNITY TARGETS
            comm_target_text = f"### Communities targeting this planet:"
            if len(planet.community_targets) > 0:
                for comm in planet.community_targets:
                    comm_target_text += (
                        f"\n-# {comm.full_name} [{comm.emoji}](<{comm.discord_link}>)"
                    )
                self.add_field(f"Communities targeting this planet:", comm_target_text)

            #LIBERATION
            liberation_text = (
                f"\n{planet.health_bar}"
                f"\n`{1 - planet.health_perc if not planet.event else planet.event.progress:^25.2%}`"
            )
            if planet.tracker and planet.tracker.change_rate_per_hour != 0:
                change = f"{planet.tracker.change_rate_per_hour:+.2%}/hr"
                liberation_text += f"\n`{change:^25}`"

            end_time_info = get_end_time(planet, gambit_planets)
            if end_time_info.end_time:
                if end_time_info.source_planet:
                    liberation_text += f"\n-# {component_json['liberated']} **<t:{int(planet.tracker.complete_time.timestamp())}:R>**"
                elif end_time_info.gambit_planet:
                    liberation_text += f"\n-# {component_json['liberated']} **<t:{int(end_time_info.gambit_planet.tracker.complete_time.timestamp())}:R>** thanks to {end_time_info.gambit_planet.names.get(lang_code, end_time_info.gambit_planet.name)} liberation"
                elif end_time_info.regions:
                    regions_list = f"\n-# ".join(
                        [
                            f" {r.emoji} {r.names.get(lang_code, r.name)}"
                            for r in end_time_info.regions
                        ]
                    )
                    liberation_text += f"\n**{component_json['liberated']}** <t:{int(end_time_info.end_time.timestamp())}:R>\nIf the following regions are liberated:\n-# {regions_list}"
            self.add_field(f"{component_json['heroes']}: **{planet.stats.player_count:,}**", liberation_text + f"\n")

    def add_mission_stats(self, planet: Planet, component_json: dict):
        self.add_field(f"{component_json['title']}",
          f"\n{component_json['missions_won']}: **{short_format(planet.stats.missions_won)}**"
        + f"\n{component_json['missions_lost']}: **{short_format(planet.stats.missions_lost)}**"
        + f"\n{component_json['missions_winrate']}: **{planet.stats.mission_success_rate}%**"
        + f"\n{component_json['missions_time_spent']}: **{planet.stats.mission_time/31556952:.1f} {component_json['years']}**"
        + f"\n"
        )

    def add_hero_stats(self, planet: Planet, component_json: dict):
        self.add_field(f"{component_json['title']}",
        f"\n{component_json['active_heroes']}: **{planet.stats.player_count:,}**"
        + f"\n{component_json['heroes_lost']}: **{short_format(planet.stats.deaths)}**"
        + f"\n{component_json['accidentals']}: **{short_format(planet.stats.friendlies)}**"
        + f"\n{component_json['shots_fired']}: **{short_format(planet.stats.bullets_fired)}**"
        + f"\n{component_json['shots_hit']}: **{short_format(planet.stats.bullets_hit)}**"
        + f"\n{component_json['accuracy']}: **{planet.stats.accuracy}%**"
        + f"\n"
        )

    def add_misc_stats(
            self, planet: Planet, component_json: dict, faction_json: dict
    ):
        faction = planet.faction if not planet.event else planet.event.faction
        if faction != Factions.humans:
            self.add_field(f"💀 {faction_json[faction.full_name]} {component_json['killed']}: ",
            f"**{short_format(getattr(planet.stats, f'{faction.singular}_kills'))}**"
            + f"\n"
            )

