from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS, VICTORY_ICONS, DEFENCE_EMBED_ICONS, ATTACK_EMBED_ICONS, URGENT_ICONS, LOSS_ICONS
from utils.api_wrapper.models import GalacticWarEffect, Planet, Campaign
from utils.dataclasses import CampaignChangesJson, PlanetFeatures, Subfaction, PlanetFeature
from utils.emojis import Emojis
from utils.mixins import EmbedReprMixin


class campaign_changes_embed(Embed, EmbedReprMixin):
    def __init__(
        self, json: CampaignChangesJson
    ):
        super().__init__(
            color=Colour.dark_theme()
        )
        self.json = json
        self.title =  f"{Emojis.Decoration.left_banner} {self.json.container['title']} {Emojis.Decoration.right_banner}"
        self.victories = ""
        self.losses = ""
        self.new_campaigns = ""
        self.planet_buttons: dict[str, str] = {}
        self.container_colours = [
            {"list": self.victories, "colour": Colour.brand_green()},
            {"list": self.losses, "colour": Colour.brand_red()},
            {
                "list": self.new_campaigns,
                "colour": Colour.from_rgb(*CUSTOM_COLOURS["MO"]),
            },
        ]


    def _add_subfactions(self, text_display: str, subfactions: set[Subfaction]):
        for sf in subfactions:
            text_display += (
                f"\n-# {sf.emoji} **{self.json.subfactions.get(sf.eng_name, sf.eng_name)}**"
            )

    def _add_regions(self, text_display: str, regions: list[Planet.Region]):
        for region in regions:
            descriptor = (
                self.json.regions[str(region.type.value)]
                if not region.is_factory
                else self.json.regions["megafactory"].format(number=region.size)
            )
            text_display += f"\n-# {region.emoji} {descriptor} **{region.names.get(self.json.lang_code_long, region.name)}**"

    def _add_features(
        self, text_display: str, planet_features: list[PlanetFeature]
    ):
        for feature in planet_features:
            text_display += f"\n-# {feature.emoji} **{feature.name}**"

    def _add_gambit(
        self,
        text_display: str,
        gambit_planet: Planet,
    ):
        if gambit_planet.regen_perc_per_hour < 0.03:
            text_display += f"\n-# :chess_pawn: {self.json.container['gambit']}: **{gambit_planet.names.get(self.json.lang_code_long, gambit_planet.name)}**"
            if gambit_planet.names.get(
                    self.json.lang_code_long, gambit_planet.name
            ) not in [self.planet_buttons.keys()]:
                self.planet_buttons.update(
                    {gambit_planet.names.get(self.json.lang_code_long, gambit_planet.name):
                         f"https://helldiverscompanion.com/#hellpad/planets/{gambit_planet.index}"})

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
            self.add_field(f"{self.json.container['victories']} {Emojis.Icons.victory}\n", self.victories)
        if self.losses != "":
            self.add_field(f"{self.json.container['losses']} {Emojis.Decoration.alert_icon}\n", self.losses)
        if self.new_campaigns != "":
            self.add_field(f"{self.json.container['new_campaigns']} {Emojis.Icons.new_icon}\n", self.new_campaigns)
        if self.planet_buttons:
            for planet_info in self.planet_buttons.keys():
                self.add_field(planet_info, self.planet_buttons[planet_info])
        self.set_thumbnail(self.thumbnail)


    def update_containers(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._update_containers()

        return wrapper

    @update_containers
    def add_liberation_victory(self, planet: Planet, taken_from: str):
        text_display = self.json.container["liberated"].format(
            planet_name=planet.names.get(self.json.lang_code_long, planet.name),
            faction_name=self.json.factions[f"{taken_from}_plural"],
        )
        self.set_thumbnail(VICTORY_ICONS.get(taken_from.lower(), VICTORY_ICONS["default"]))
        self._add_features(
            text_display=text_display,
            planet_features=planet.planet_features,
        )
        self._add_subfactions(
            text_display=text_display,
            subfactions=planet.subfactions,
        )
        self.victories += "\n"
        self.victories += text_display

        if planet.names.get(
            self.json.lang_code_long, planet.name
        ) not in [self.planet_buttons.keys()]:
            self.planet_buttons.update({planet.names.get(self.json.lang_code_long, planet.name):
                f"https://helldiverscompanion.com/#hellpad/planets/{planet.index}"})

    @update_containers
    def add_defence_victory(
        self, planet: Planet, defended_against: str, hours_remaining: int
    ):
        text_display = self.json.container["defended"].format(
            planet_name=planet.names.get(self.json.lang_code_long, planet.name),
            faction_name=self.json.factions[f"{defended_against}_plural"],
        )
        self.set_thumbnail(VICTORY_ICONS.get(defended_against.lower(), VICTORY_ICONS["default"]))
        if hours_remaining != 0:
            text_display += self.json.container[
                "ahead_of_schedule"
            ].format(
                hours_remaining=f"{hours_remaining:.0f}",
            )
        self._add_features(
            text_display=text_display,
            planet_features=planet.planet_features,
        )
        self._add_subfactions(
            text_display=text_display,
            subfactions=planet.subfactions,
        )
        self.victories += "\n"
        self.victories += text_display

        if planet.names.get(
            self.json.lang_code_long, planet.name
        ) not in [self.planet_buttons.keys()]:
            self.planet_buttons.update({planet.names.get(self.json.lang_code_long, planet.name):
                f"https://helldiverscompanion.com/#hellpad/planets/{planet.index}"})

    @update_containers
    def add_new_campaign(self, campaign: Campaign, gambit_planets: dict[int, Planet]):
        if campaign.planet.event:
            text_display = self.json.container["defend"].format(
                planet_name=campaign.planet.names.get(
                    self.json.lang_code_long, campaign.planet.name
                ),
                emojis=campaign.planet.exclamations,
            )
            text_display += self.json.container["invasion_level"].format(
                level=campaign.planet.event.level,
                emoji=campaign.planet.event.level_exclamation,
            )
            text_display += self.json.container["ends"].format(
                timestamp=int(
                    campaign.planet.event.end_time_datetime.timestamp()
                )
            )
            self.set_thumbnail(
                DEFENCE_EMBED_ICONS.get(
                    campaign.planet.event.faction.full_name.lower(),
                    DEFENCE_EMBED_ICONS["default"],
                ))
            self._add_features(
                text_display=text_display,
                planet_features=campaign.planet.planet_features,
            )

            self._add_subfactions(
                text_display=text_display,
                subfactions=campaign.planet.subfactions,
            )

            self._add_regions(
                text_display=text_display,
                regions=campaign.planet.regions.values(),
            )

            if campaign.planet.index in gambit_planets:
                self._add_gambit(
                    text_display=text_display,
                    gambit_planet=gambit_planets[campaign.planet.index],
                )

            # last step
            self.new_campaigns += "\n"
            self.new_campaigns += text_display

            if campaign.planet.names.get(
                    self.json.lang_code_long, campaign.planet.name
            ) not in [self.planet_buttons.keys()]:
                self.planet_buttons.update({campaign.planet.names.get(self.json.lang_code_long, campaign.planet.name):
                    f"https://helldiverscompanion.com/#hellpad/planets/{campaign.planet.index}"})
        else:
            text_display = self.json.container["liberate"].format(
                planet_name=campaign.planet.names.get(
                    self.json.lang_code_long, campaign.planet.name
                ),
                emojis=campaign.faction.emoji + campaign.planet.exclamations,
                )
            text_display += self.json.container["resistance"].format(
                regen=f"{campaign.planet.regen_perc_per_hour:+.2%}"
            )
            self.set_thumbnail(
                ATTACK_EMBED_ICONS.get(
                    campaign.faction.full_name.lower(),
                    ATTACK_EMBED_ICONS["default"],
                ))
            self._add_features(
                text_display=text_display,
                planet_features=campaign.planet.planet_features,
            )
            self._add_subfactions(
                text_display=text_display,
                subfactions=campaign.planet.subfactions,
            )
            self._add_regions(
                text_display=text_display,
                regions=campaign.planet.regions.values(),
            )

            # last step
            self.new_campaigns += "\n"
            self.new_campaigns += text_display

            if campaign.planet.names.get(
                    self.json.lang_code_long, campaign.planet.name
            ) not in [self.planet_buttons.keys()]:
                self.planet_buttons.update({campaign.planet.names.get(self.json.lang_code_long, campaign.planet.name):
                    f"https://helldiverscompanion.com/#hellpad/planets/{campaign.planet.index}"})

    @update_containers
    def new_urgent_liberation(
        self, campaign: Campaign, gambit_planets: dict[int, Planet]
    ):
        text_display = self.json.container["urgently_liberate"].format(
            planet_name=campaign.planet.names.get(
                self.json.lang_code_long, campaign.planet.name
            ),
            emojis=campaign.planet.exclamations,
        )
        text_display += self.json.container["urgency_level"].format(
            level=campaign.planet.event.level,
            emoji=campaign.planet.event.level_exclamation,
        )
        text_display += self.json.container["ends"].format(
            timestamp=int(
                campaign.planet.event.end_time_datetime.timestamp()
            )
        )
        self.set_thumbnail(
            URGENT_ICONS.get(
                campaign.planet.event.faction.full_name.lower(),
                URGENT_ICONS["default"],
            ))
        self._add_features(
            text_display=text_display,
            planet_features=campaign.planet.planet_features,
        )

        self._add_subfactions(
            text_display=text_display,
            subfactions=campaign.planet.subfactions,
        )

        self._add_regions(
            text_display=text_display,
            regions=campaign.planet.regions.values(),
        )

        if campaign.planet.index in gambit_planets:
            self._add_gambit(
                text_display=text_display,
                gambit_planet=gambit_planets[campaign.planet.index],
            )

        # last step
        self.new_campaigns += "\n"
        self.new_campaigns += text_display

        if campaign.planet.names.get(
                self.json.lang_code_long, campaign.planet.name
        ) not in [self.planet_buttons.keys()]:
            self.planet_buttons.update({campaign.planet.names.get(self.json.lang_code_long, campaign.planet.name):
                f"https://helldiverscompanion.com/#hellpad/planets/{campaign.planet.index}"})

    @update_containers
    def add_planet_lost(self, planet: Planet):
        text_display = self.json.container["planet_lost"].format(
            planet_name=planet.names.get(self.json.lang_code_long, planet.name),
            emojis=planet.exclamations,
            faction_name=self.json.factions[
                f"{planet.faction.full_name}_plural"
            ],
        )
        self.set_thumbnail(LOSS_ICONS.get(planet.faction.full_name.lower(), LOSS_ICONS["default"]))
        self._add_features(
            text_display=text_display,
            planet_features=planet.planet_features,
        )
        self._add_subfactions(
            text_display=text_display,
            subfactions=planet.subfactions,
        )
        self.losses += "\n"
        self.losses += text_display

        if planet.names.get(
                self.json.lang_code_long, planet.name
        ) not in [self.planet_buttons.keys()]:
            self.planet_buttons.update({planet.names.get(self.json.lang_code_long, planet.name):
                f"https://helldiverscompanion.com/#hellpad/planets/{planet.index}"})
