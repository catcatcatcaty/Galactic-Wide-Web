from disnake import Embed, Colour

from utils.dbv2 import GWWGuild
from utils.mixins import EmbedReprMixin


FEATURE_TYPES = [
    "api_changes",
    "dashboards",
    "maps",
    "detailed_dispatches",
    "dss_announcements",
    "major_order_updates",
    "patch_notes",
    "region_announcements",
    "war_announcements"
]

class settings_embed(Embed, EmbedReprMixin):
    def __init__(
        self,
        guild: GWWGuild,
        setting: bool,
    ):
        super().__init__(title="Settings :gear:", color=Colour.dark_theme())
        self.guild = guild
        self.setting = setting
        if setting:
            self.set_footer(text="Setting saved! :white_check_mark:")
            return

        text_display = ""
        for feature_type in FEATURE_TYPES:
            text_display += f"Feature `{feature_type}`: "
            features = [f for f in guild.features if f.name == feature_type]
            feature = features[0] if len(features) > 0 else None
            text_display += f":white_check_mark: enabled in <#{feature.channel_id}>\n" if feature is not None else ":x: disabled \n"

        self.add_field("Features:", text_display)
        self.add_field("Language:", f"{guild.language}", inline=False)
        self.add_field("-", "Use: `!setup <feature>` (in relevant channel) or `!setup language <language>` to configure. \nOr use `!setup reset <feature>` or `!setup reset_all` to clear settings.", inline=False)