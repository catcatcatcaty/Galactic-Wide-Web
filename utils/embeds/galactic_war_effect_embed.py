from disnake import Embed, Colour

from utils.api_wrapper.models import GalacticWarEffect, Planet
from utils.dataclasses import PlanetFeatures, Subfactions
from utils.mixins import EmbedReprMixin


class galactic_war_effect_embed(Embed, EmbedReprMixin):
    def __init__(
        self,
        gwe: GalacticWarEffect,
        planets_with_gwe: list[Planet] | str,
        with_planets_list: bool = True,
        with_pretty_print: bool = True,
    ):
        super().__init__(
            colour=Colour.dark_theme()
        )
        self.add_field(f"{gwe.id} - {gwe.effect_description['simplified_name']}", "-")

        content = ""
        if gwe.name is not None:
            content += f"\n**{gwe.name}**"
        if gwe.short_description is not None:
            content += f"\n{gwe.short_description}"
        if gwe.long_description is not None:
            content += f"\n-# {gwe.long_description}"
        if gwe.fluff_description is not None:
            content += f"\n-# {gwe.fluff_description}"
        if gwe.resource is not None:
            content += f"\n{gwe.resource}"

        if feature := PlanetFeatures.all.get(gwe.id) is not None:
            content += f"\n**{feature.name}** {feature.emoji}"

        if (
            subfaction_poi := next(
                (sf for sf in Subfactions._all if sf.token_effect_id == gwe.id), None
            )
        ) is not None:
            content += f"\n**{subfaction_poi.eng_name}** {subfaction_poi.emoji}"

        if gwe.found_enemy is not None and gwe.found_enemy.upper() not in content:
            if (
                subfaction := next(
                    (
                        sf
                        for sf in Subfactions._all
                        if sf.resource_hash == gwe.resource_hash
                    ),
                    None,
                )
            ) is not None:
                enemy_text = f"**{subfaction.eng_name}** {subfaction.emoji}"
            else:
                enemy_text = f"**{gwe.found_enemy}**"
            content += f"\nEnemy: {enemy_text}"

        if gwe.found_stratagem is not None and gwe.found_stratagem not in content:
            content += f"\nStratagem: **{gwe.found_stratagem}**"

        if gwe.stratagem_category is not None:
            content += f"\nStratagem Category: **{gwe.stratagem_category}**"

        if gwe.found_booster is not None and gwe.found_booster not in content:
            content += f"\nBooster: **{gwe.found_booster}**"

        if gwe.count is not None:
            count = "Count" if gwe.effect_type != 32 else "Uses per mission"
            amount = f"{gwe.count:+,}"
            if gwe.count == 0:
                amount = "Infinite"
            content += f"\n{count}: **{amount}**"
        if gwe.percent is not None:
            percent = gwe.percent
            match gwe.effect_type:
                case 1 | 72:
                    percent -= 100
            content += f"\nPercent: **{percent:+,}%**"

        if with_planets_list:
            active_planets = ""
            if isinstance(planets_with_gwe, str):
                active_planets = "-# ALL PLANETS"
            elif planets_with_gwe:
                active_planets = "-# " + "\n-# ".join(
                    [f"#{p.index} - {p.name}" for p in planets_with_gwe]
                )
            else:
                active_planets = "-# None"
            content += f"\n**Active on**\n{active_planets}"


        self.add_field("-", content)

        if with_pretty_print:
            self.add_field(f"\n```py\n{gwe}```", "-")