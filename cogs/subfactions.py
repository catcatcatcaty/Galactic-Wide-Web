from disnake import (
    AppCmdInter,
    ApplicationInstallTypes,
    InteractionContextTypes,
    MessageInteraction,
)
from disnake.ext import commands
from disnake.ext.commands import Command

from main import GalacticWideWebBot
from utils.checks import wait_for_startup
from utils.containers import SubfactionsContainer
from utils.dataclasses import Subfactions
from utils.dataclasses.factions import Factions
from utils.dbv2 import GWWGuild, GWWGuilds
from utils.embeds.subfactions_embed import subfactions_embed


class SubfactionCog(commands.Cog):
    def __init__(self, bot: GalacticWideWebBot) -> None:
        self.bot = bot

    @wait_for_startup()
    @commands.slash_command(
        description="Get information on enemy subfactions and their controlled planets",
        install_types=ApplicationInstallTypes.all(),
        contexts=InteractionContextTypes.all(),
        extras={
            "long_description": "Shows the subfaction with the most controlled planets by default, along with a list of the planets they currently occupy. Use the dropdown to switch between subfactions.",
            "example_usage": "**`/subfaction public:Yes`** returns the most widespread subfaction and their planets, visible to everyone. Use the dropdown to view other subfactions.",
        },
    )
    async def subfaction(
        self,
        inter: AppCmdInter,
        public: str = commands.Param(
            choices=["Yes", "No"],
            default="No",
            description="If you want the response to be seen by others in the server.",
        ),
    ) -> None:
        await inter.response.defer(ephemeral=public != "Yes")
        if inter.guild:
            guild = GWWGuilds.get_specific_guild(id=inter.guild_id)
            if not guild:
                self.bot.logger.error(
                    f"Guild {inter.guild_id} - {inter.guild.name} - had the bot installed but wasn't found in the DB"
                )
                guild = GWWGuilds.add(inter.guild_id, "en", [])
        else:
            guild = GWWGuild.default()

        sf_planetcount_tuples = [
            (
                sf,
                len(
                    [
                        p
                        for p in self.bot.data.formatted_data.planets.values()
                        if sf in p.subfactions
                        and (p.faction != Factions.humans or p.active_campaign)
                    ]
                ),
            )
            for sf in Subfactions._all
        ]
        subfaction_to_use = max(sf_planetcount_tuples, key=lambda x: x[1])[0]
        container = SubfactionsContainer(
            subfaction=subfaction_to_use, planets=self.bot.data.formatted_data.planets
        )
        await inter.send(components=container)

    @commands.Cog.listener("on_dropdown")
    async def subfactions_listener(self, inter: MessageInteraction):
        if (
            not self.bot.ready
            or inter.component.custom_id != "subfactions"
            or inter.author != inter.message.interaction_metadata.user
        ):
            return
        subfaction = next(
            (
                sf
                for sf in Subfactions._all
                if sf.eng_name.title() == inter.values[0].split(" - ")[0]
            ),
            None,
        )
        if inter.guild:
            guild = GWWGuilds.get_specific_guild(id=inter.guild_id)
            if not guild:
                self.bot.logger.error(
                    f"Guild {inter.guild_id} - {inter.guild.name} - had the bot installed but wasn't found in the DB"
                )
                guild = GWWGuilds.add(inter.guild_id, "en", [])
        else:
            guild = GWWGuild.default()
        container = SubfactionsContainer(
            subfaction=subfaction, planets=self.bot.data.formatted_data.planets
        )
        await inter.response.edit_message(components=container)

###FLUXER


    @wait_for_startup()
    @commands.command("subfactions", Command, rest_is_raw=True)
    async def subfactions(
            self,
            ctx: commands.Context,
            *,
            arg) -> None:
        if ctx.guild:
            guild = GWWGuilds.get_specific_guild(id=ctx.guild.id)
            if not guild:
                self.bot.logger.error(
                    f"Guild {ctx.guild.id} - {ctx.guild.name} - had the bot installed but wasn't found in the DB"
                )
                guild = GWWGuilds.add(ctx.guild.id, "en", [])
        else:
            guild = GWWGuild.default()
        sf_planetcount_tuples = [
            (
                sf,
                len(
                    [
                        p
                        for p in self.bot.data.formatted_data.planets.values()
                        if sf in p.subfactions
                           and (p.faction != Factions.humans or p.active_campaign)
                    ]
                ),
            )
            for sf in Subfactions._all
        ]
        subfaction_to_use = max(sf_planetcount_tuples, key=lambda x: x[1])[0]
        if arg:
            subfaction_to_use = next(
                (
                    sf
                    for sf in Subfactions._all
                    if sf.eng_name.lower() == arg[1:].lower().replace("_", " ")
                ),
                None,
            )
            if subfaction_to_use is None:
                subfactions_all = []
                for p in self.bot.data.formatted_data.planets.values():
                    for sf in p.subfactions:
                        if (p.faction != Factions.humans or p.active_campaign) and sf.eng_name.title() + ", " not in subfactions_all:
                            subfactions_all.append(sf.eng_name.title() + ", ")
                await ctx.send(f":warning: Value must be one of: " + "".join(subfactions_all))
                return
        container = subfactions_embed(
            subfaction=subfaction_to_use, planets=self.bot.data.formatted_data.planets
        )
        if not arg:
            container.set_footer(text="Showing largest currently active Subfaction - Specify an active Subfaction (or \"all\") as a command argument to see others!")
        await ctx.send(embed=container)




def setup(bot: GalacticWideWebBot) -> None:
    bot.add_cog(SubfactionCog(bot))
