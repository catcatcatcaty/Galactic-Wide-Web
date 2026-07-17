from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS
from utils.api_wrapper.models import Dispatch
from utils.mixins import EmbedReprMixin


class dispatch_embed(Embed, EmbedReprMixin):
    def __init__(
        self, dispatch_json: dict, dispatch: Dispatch, with_time: bool = False
    ):
        super().__init__(
            accent_colour=Colour.from_rgb(*CUSTOM_COLOURS["MO"]),
        )

        title, description = dispatch.title, dispatch.description
        if description and title:
            self.add_field(f"# {title}", f"\n{description}")
        if with_time:
            self.add_field(".", dispatch_json["with_time"].format(
                timestamp=int(dispatch.published_at.timestamp())))
        self.add_field(".", f"\n-# {dispatch_json['dispatch']} #{dispatch.id}")

