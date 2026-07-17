from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS
from utils.api_wrapper.models import GalacticWarEffect, Planet
from utils.dataclasses import CampaignChangesJson, SpecialUnits, PlanetFeatures
from utils.emojis import Emojis
from utils.mixins import EmbedReprMixin


class dispatch_embed(Embed, EmbedReprMixin):
    def __init__(
        self, json: CampaignChangesJson
    ):
        super().__init__(
            color=Colour.dark_theme()
        )
        self.json = json
        self.title =  f"# {Emojis.Decoration.left_banner} {self.json.container['title']} {Emojis.Decoration.right_banner}"
        self.victories = [
            (
                f"## {self.json.container['victories']} {Emojis.Icons.victory}"
            )
        ]
        self.losses = [
            (
                f"## {self.json.container['losses']} {Emojis.Decoration.alert_icon}"
            ),
        ]
        self.new_campaigns = [
            (
                f"## {self.json.container['new_campaigns']} {Emojis.Icons.new_icon}"
            )
        ]
        self.container_colours = [
            {"list": self.victories, "colour": Colour.brand_green()},
            {"list": self.losses, "colour": Colour.brand_red()},
            {
                "list": self.new_campaigns,
                "colour": Colour.from_rgb(*CUSTOM_COLOURS["MO"]),
            },
        ]

    def _add_special_units(
        self, embed: Embed, active_effects: set[GalacticWarEffect]
    ):
        for su_name, su_emoji in SpecialUnits.get_from_effects_list(
            active_effects=active_effects
        ):
            embed.add_field(".", f"\n-# {su_emoji} **{self.json.special_units[su_name]}**"
            )

    def _add_regions(self, embed: Embed, regions: list[Planet.Region]):
        for region in regions:
            embed.add_field(".", f"\n-# {region.emoji} {self.json.regions[str(region.type.value)]} **{region.names[self.json.lang_code_long]}**")

    def _add_features(
        self, embed: Embed, active_effects: set[GalacticWarEffect]
    ):
        for feature_name, feature_emoji in PlanetFeatures.get_from_effects_list(
            active_effects
        ):
            embed.add_field(".", f"\n-# {feature_emoji} **{feature_name}**")

    def _add_gambit(
        self,
        embed: Embed,
        gambit_planet: Planet,
    ):
        if gambit_planet.regen_perc_per_hour < 0.03:
            embed.add_field(".", f"\n-# :chess_pawn: {self.json.container['gambit']}: **{gambit_planet.names.get(self.json.lang_code_long, gambit_planet.index)}**")
            if gambit_planet.names.get(
                self.json.lang_code_long, str(gambit_planet.index)
            ) not in [b.label for b in self.planet_buttons]:
                embed.add_field(str(gambit_planet.names.get(
                            self.json.lang_code_long, str(gambit_planet.index))), f"https://helldiverscompanion.com/#hellpad/planets/{gambit_planet.index}")

    #what does this even do
    def _update_containers(self):
        colour = Colour.dark_theme()
        longest_length = 0
        for container_info in self.container_colours:
            if len(container_info["list"]) - 1 > longest_length:
                longest_length = len(container_info["list"]) - 1
                colour = container_info["colour"]
        planet_button_chunks = [
            self.planet_buttons[i: i + 3]
            for i in range(0, len(self.planet_buttons), 3)
        ]
        """
        super().__init__(
            *(
                    self.title
                    + self.non_empty_components
                    + (
                        [ui.ActionRow(*chunk) for chunk in planet_button_chunks]
                        if self.planet_buttons
                        else []
                    )
            ),
            accent_colour=colour,
        )
        """
        #pretend it works for now
        embed = super().__init__(
            color=colour,
            title=self.title
        )
        for text in self.non_empty_components:
            embed.add_field(text, ".")


    def update_containers(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._update_containers()

        return wrapper

    @property
    def non_empty_components(self):
        results = []
        for list_ in [self.victories, self.losses, self.new_campaigns]:
            if len(list_) > 1:
                results.extend(list_)
        return results

    @property
    def components(self) -> list:
        return self.victories + self.losses + self.new_campaigns
