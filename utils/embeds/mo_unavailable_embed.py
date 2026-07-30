from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS
from utils.mixins import EmbedReprMixin


class mo_unavilable_embed(Embed, EmbedReprMixin):
    def __init__(
        self,
    ):
        super().__init__(
            colour=Colour.from_rgb(*CUSTOM_COLOURS["MO"])
        )
        self.add_field(f"Awaiting Major Order\nStand by for further orders from Super Earth High Command", "-")
        self.set_thumbnail("https://fluxerusercontent.com/attachments/1476525402340249794/1530873086176403456/1000108515.png")