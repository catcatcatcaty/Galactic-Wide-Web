###FLUXER
from disnake import Embed, Colour
from disnake.ext import commands
from disnake.ext.commands import Cog

from data.lists import CUSTOM_COLOURS
from utils.bot import GalacticWideWebBot
from utils.checks import wait_for_startup
from utils.dbv2 import GWWGuilds, GWWGuild
from utils.emojis import Emojis


class InviteCog(Cog):
    def __init__(self, bot: GalacticWideWebBot) -> None:
        self.bot = bot

    @wait_for_startup()
    @commands.command("invite")
    async def invite(
            self,
            ctx: commands.Context,
    ) -> None:
        if ctx.guild:
            guild = GWWGuilds.get_specific_guild(id=ctx.guild.id)
            if not guild:
                self.bot.logger.error(
                    f"Guild {ctx.guild.id} - {ctx.guild.name} - had the bot installed but wasn't found in the DB"
                )
                guild = GWWGuilds.add(ctx.guild.id, "en", [])
        else:
            guild = GWWGuild.default()
        embed = Embed(color=Colour.from_rgb(*CUSTOM_COLOURS["MO"]))
        embed.add_field(f"{Emojis.Icons.discord} Add the bot to your server:", "https://web.fluxer.app/oauth2/authorize?client_id=1476519709822349355&scope=bot")
        embed.add_field(f"{Emojis.Icons.discord} Join the Galactic Wide Web: Fluxer Port support server:", "https://fluxer.gg/m50i6kcZ")
        embed.set_thumbnail("https://fluxerusercontent.com/attachments/1476525402340249794/1531225330679820288/1000108601.png")
        await ctx.send(embed=embed)

def setup(bot: GalacticWideWebBot) -> None:
        bot.add_cog(InviteCog(bot))