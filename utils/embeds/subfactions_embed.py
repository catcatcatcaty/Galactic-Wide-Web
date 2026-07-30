from disnake import Embed, Colour

from utils.api_wrapper.models import Planet
from utils.dataclasses import Subfaction, Factions
from utils.mixins import EmbedReprMixin


class subfactions_embed(Embed, EmbedReprMixin):
    def __init__(self, subfaction: Subfaction, planets: dict[int, Planet]):

        text_display = ""
        if planets_with_sf := sorted(
                [
                    p
                    for p in planets.values()
                    if subfaction in p.subfactions
                       and (p.faction != Factions.humans or p.active_campaign)
                ],
                key=lambda x: x.stats.player_count,
                reverse=True,
        ):
            for planet in planets_with_sf:
                text_display += f"\n- {planet.faction.emoji} {planet.name}"
                text_display += f"\n-# {planet.stats.player_count:,} Heroes"
                text_display += f"\nhttps://helldiverscompanion.com/#hellpad/planets/{planet.index}"
            colour = max(
                [p.faction for p in planets_with_sf],
                key=[p.faction for p in planets_with_sf].count,
            ).colour
        else:
            text_display += f"- None"
            colour = Factions.humans.colour
        super().__init__(
            colour=Colour.from_rgb(*colour),
        )
        self.title = f"{subfaction.emoji} {subfaction.eng_name.title()}"
        self.add_field(f"Planets with this subfaction active:", text_display)