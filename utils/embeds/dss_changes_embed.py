from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS
from utils.api_wrapper.models import Planet, DSS
from utils.dataclasses import DSSChangesJson, Subfaction, PlanetFeature
from utils.emojis import Emojis
from utils.functions import short_format
from utils.mixins import EmbedReprMixin

STATUSES = {0: "inactive", 1: "preparing", 2: "active", 3: "on_cooldown"}

AMOUNT_PER_COST = {
    "Requisition Slip": 50_000,
    "Common Sample": 75,
    "Rare Sample": 50,
}

class dss_changes_embed(Embed, EmbedReprMixin):
    def __init__(
        self,
        json: DSSChangesJson,
    ):
        self.json = json
        super().__init__(
        color=Colour.from_rgb(*CUSTOM_COLOURS["DSS"]),
        title= f"{self.json.container['title']} {Emojis.SpaceStations.DSS.icon}"
        )
    text_display = ""

    def _add_subfactions(self, text_display: str, subfactions: set[Subfaction]):
        for sf in subfactions:
            text_display += (
                f"\n-# {sf.emoji} **{self.json.subfactions[sf.eng_name]}**"
            )

    def _add_regions(self, text_display: str, regions: list[Planet.Region]):
        for region in sorted(regions, key=lambda x: x.availability_factor):
            region_type = (
                self.json.regions[str(region.type.value)]
                if not region.is_factory
                else self.json.regions["megafactory"].format(number=region.type.value)
            )
            text_display += f"\n-# {region.emoji} {region_type} **{region.names.get(self.json.lang_code_long, region.name)}**"

    def _add_features(
        self, text_display: str, planet_features: list[PlanetFeature]
    ):
        for feature in planet_features:
            text_display += f"\n-# {feature.emoji} {feature.name}"

    def _add_gambit(
        self,
        text_display: str,
        gambit_planet: Planet,
    ):
        if gambit_planet.regen_perc_per_hour < 0.03:
            text_display += f"\n-# {self.json.container['gambit']}: {gambit_planet.names.get(self.json.lang_code_long, gambit_planet.name)}"

    def _update_containers(self):
        super().__init__(
            title=self.title,
            colour=self.colour
        )
        self.clear_fields()
        self.add_field("-", self.text_display)


    def update_containers(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._update_containers()

        return wrapper

    @update_containers
    def dss_moved(self, before_planet: Planet, after_planet: Planet):
        text_display = self.json.container["has_moved"].format(
            planet_name1=before_planet.names.get(
                self.json.lang_code_long, before_planet.name
            ),
            planet_name2=after_planet.names.get(
                self.json.lang_code_long, after_planet.name
            ),
            emojis=after_planet.exclamations,
            )
        self._add_features(
            text_display=text_display,
            planet_features=after_planet.planet_features,
        )
        self._add_subfactions(
            text_display=text_display,
            subfactions=after_planet.subfactions,
        )
        self._add_regions(
            text_display=text_display,
            regions=after_planet.regions.values(),
        )

        self.text_display += "\n"
        self.text_display += text_display

    @update_containers
    def ta_status_changed(self, tactical_action: DSS.TacticalAction):
        text_display = self.json.container["ta_status_change"].format(
            ta_name=self.json.container["tactical_actions"]
            .get(tactical_action.name, {})
            .get("name", tactical_action.name),
            status=self.json.container[STATUSES[tactical_action.status]],
        )
        if tactical_action.status == 1:
            for cost in tactical_action.cost:
                text_display += self.json.container[
                    "required_cost"
                ].format(
                    amount=short_format(cost.target * AMOUNT_PER_COST[cost.item]),
                    item_name=self.json.currencies.get(cost.item, cost.item),
                )
        elif tactical_action.status == 2:
            text_display += (
                f"\n{self.json.container['tactical_actions'].get(tactical_action.name, {}).get('description', tactical_action.description)}"
                + f"\n{self.json.container['expires']} <t:{int(tactical_action.status_end_datetime.timestamp())}:R>"
            )
        elif tactical_action.status == 3:
            text_display += f"\n-# {self.json.container['prep_starts']} **<t:{int(tactical_action.status_end_datetime.timestamp())}:R>**"

        self.text_display += "\n"
        self.text_display += text_display