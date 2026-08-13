from disnake import Embed, Colour

from data.lists import VICTORY_ICONS, CUSTOM_COLOURS, ATTACK_EMBED_ICONS
from utils.api_wrapper.models import Planet
from utils.dataclasses import RegionChangesJson, Subfaction, PlanetFeature
from utils.emojis import Emojis
from utils.mixins import EmbedReprMixin


class region_changes_embed(Embed, EmbedReprMixin):
    def __init__(
        self,
        container_json: RegionChangesJson,
    ):
        super().__init__(
        color=Colour.dark_theme(),
        )
        self.container_json = container_json
        self.title = f"{Emojis.Decoration.left_banner} {self.container_json.container['title']} {Emojis.Decoration.right_banner}"

        self.victories = ""
        self.new_regions = ""
        self.planet_buttons: dict[str, str] = {}
        self.container_colours = [
            {"list": self.victories, "colour": Colour.brand_green()},
            {
                "list": self.new_regions,
                "colour": Colour.from_rgb(*CUSTOM_COLOURS["MO"]),
            },
        ]

    def _add_subfactions(self, text_display: str,  subfactions: set[Subfaction]):
        for sf in subfactions:
            text_display += f"\n-# {sf.emoji} **{self.container_json.subfactions.get(sf.eng_name, sf.eng_name)}**"

    def _add_features(self, text_display: str, planet_features: list[PlanetFeature]):
        for feature in planet_features:
            text_display += f"\n-# {feature.emoji} {feature.name}"

    def _update_containers(self):
        colour = Colour.dark_theme()
        longest_length = 0
        for container_info in self.container_colours:
            if len(container_info["list"]) - 1 > longest_length:
                longest_length = len(container_info["list"]) - 1
                colour = container_info["colour"]
        super().__init__(
            title=self.title,
            colour=colour,
        )
        self.clear_fields()
        if self.victories != "":
            self.add_field(f"{self.container_json.container['victories']} {Emojis.Icons.victory}", self.victories)
        if self.new_regions != "":
            self.add_field(f"{self.container_json.container['new_regions']} {Emojis.Icons.new_icon}", self.new_regions)
        if self.planet_buttons:
            planets_text = ""
            for planet_info in self.planet_buttons.keys():
                planets_text += f"{planet_info}: {self.planet_buttons[planet_info]}\n"
            self.add_field("-", planets_text)
        self.set_thumbnail(self.thumbnail)

    def update_containers(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._update_containers()
        return wrapper

    @update_containers
    def add_region_victory(self, region: Planet.Region):
        text_display = self.container_json.container["region_victory"].format(
                region_emoji=region.emoji,
                region_name=region.names.get(
                    self.container_json.lang_code_long, region.name
                ),
                planet_name=region.planet.names.get(
                    self.container_json.lang_code_long, region.planet.name
                ),
                faction_name=self.container_json.factions[
                    (
                        f"{region.planet.faction.full_name}_plural"
                        if not region.planet.event
                        else f"{region.planet.event.faction.full_name}_plural"
                    )
                ],
        )
        self.set_thumbnail(VICTORY_ICONS.get(
            (
                region.planet.faction.full_name.lower()
                if not region.planet.event
                else region.planet.event.faction.full_name.lower()
            ),
            VICTORY_ICONS["default"],
        ))
        self._add_features(
            text_display=text_display,
            planet_features=region.planet.planet_features,
        )
        self._add_subfactions(
            text_display=text_display,
            subfactions=region.planet.subfactions,
        )
        self.victories += "\n"
        self.victories += text_display

        if region.planet.names.get(
            self.container_json.lang_code_long, region.planet.name
        ) not in [self.planet_buttons.keys()]:
            self.planet_buttons.update({region.planet.names.get(self.container_json.lang_code_long, region.planet.name):
                f"https://helldiverscompanion.com/#hellpad/planets/{region.planet.index}"})


    @update_containers
    def add_new_region(self, region: Planet.Region):
        text_display = self.container_json.container["new_region"].format(
            region_emoji=region.emoji,
            region_name=region.names.get(
                self.container_json.lang_code_long, region.name
            ),
            planet_name=region.planet.names.get(
                self.container_json.lang_code_long, region.planet.name
                ),
        )
        text_display += self.container_json.container["resistance"].format(
            regen=f"{region.regen_perc_per_hour:.2%}"
        )
        self.set_thumbnail(
            ATTACK_EMBED_ICONS.get(
                (
                    region.planet.faction.full_name.lower()
                    if not region.planet.event
                    else region.planet.event.faction.full_name.lower()
                ),
                ATTACK_EMBED_ICONS["default"],
            )
        ),
        if region.description:
            text_display += f"\n-# {region.descriptions[self.container_json.lang_code_long]}"
        self._add_features(
            text_display=text_display,
            planet_features=region.planet.planet_features,
        )
        self._add_subfactions(
            text_display=text_display,
            subfactions=region.planet.subfactions,
        )

        self.new_regions += "\n"
        self.new_regions += text_display

        if region.planet.names.get(
            self.container_json.lang_code_long, region.planet.name
        ) not in [self.planet_buttons.keys()]:
            self.planet_buttons.update({region.planet.names.get(self.container_json.lang_code_long, region.planet.name):
                f"https://helldiverscompanion.com/#hellpad/planets/{region.planet.index}"})