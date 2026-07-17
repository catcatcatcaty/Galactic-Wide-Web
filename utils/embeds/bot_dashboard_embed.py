from datetime import datetime
from math import inf
from os import getpid

from disnake import Embed, Colour
from psutil import Process, net_io_counters, cpu_percent

from utils.bot import GalacticWideWebBot
from utils.mixins import EmbedReprMixin


class bot_dashboardEmbed(Embed, EmbedReprMixin):
    def __init__(
        self,
        bot: GalacticWideWebBot
    ):
        super().__init__(
        )

        now = datetime.now()
        commands_text = ""
        for global_command in sorted(bot.commands, key=lambda sc: sc.name):
            if global_command.name not in ["gwe", "global_event"]:
                commands_text += f"- {global_command.name}\n"
        self.add_field( f"The GWW has {len([c for c in bot.commands if c.name not in ['gwe', 'global_event']])} commands available", commands_text)

        servers_by_age = sorted([g for g in bot.guilds], key=lambda x: x.created_at)
        oldest_server = servers_by_age[0]
        newest_server = servers_by_age[-1]
        community_servers = len([g for g in bot.guilds if "COMMUNITY" in g.features])
        member_count = sum(guild.member_count for guild in bot.guilds)
        text_channels = sum(len(g.text_channels) for g in bot.guilds)
        voice_channels = sum(len(g.voice_channels) for g in bot.guilds)
        total_emojis = sum(len(g.emojis) for g in bot.guilds)
        self.add_field(f"Servers: **{len(bot.guilds):,}**",
                        f"\n-# ├ Newest Server: Created **<t:{int(newest_server.created_at.timestamp())}:R>**"
                        + f"\n-# ├ Oldest Server: Created **<t:{int(oldest_server.created_at.timestamp())}:R>**"
                        + f"\n-# └ Community Servers: **{community_servers:,}**"
                        + f"\nMembers of Democracy: **{member_count:,}**"
                        + f"\nTotal Channels"
                        + f"\n-# ├ Text: **{text_channels:,}**"
                        + f"\n-# └ Voice: **{voice_channels:,}**"
                        + f"\nEmojis: **{total_emojis:,}**")

        memory_used = Process(getpid()).memory_info().rss / 1024**2
        latency = 9999.999 if bot.latency == float(inf) else bot.latency
        self.add_field(":desktop: Hardware Info", f"-# **CPU**: {cpu_percent()}%\n-# **RAM**: {memory_used:.2f}MB\n-# **Last restart**: <t:{int(bot.startup_time.timestamp())}:R>\n-# **Latency**: {int(latency * 1000)}ms")

        net_io = net_io_counters()
        bytes_sent_gb = net_io.bytes_sent / (1024**3)
        bytes_recv_gb = net_io.bytes_recv / (1024**3)

        self.add_field(":satellite: Network Info", f"-# **Sent**: {bytes_sent_gb:.2f}GB\n-# **Received:** {bytes_recv_gb:.2f}GB")

        shardinfo = "\n".join(
            [
                f"-# **#{shard.id + 1}** - **{shard.latency * 1000:.0f}ms** - {len([g for g in bot.guilds if g.shard_id == shard.id])} Guilds"
                for shard in bot.shards.values()
            ]
        )
        self.add_field(":jigsaw: Shards", f"{shardinfo}")

        loop_errors = ""
        embed_colours = {
            0: Colour.brand_green(),
            1: Colour.orange(),
            2: Colour.brand_red(),
        }
        errors = 0
        for loop in bot.loops:
            if not loop.is_running() and not loop.count:
                loop_errors += f"{loop.coro.__name__} - **__ERROR__**:warning:\n"
                errors += 1
        if loop_errors:
            self.add_field("LOOP ERRORS", f"{loop_errors}")
        self.colour = embed_colours.get(errors, Colour.from_rgb(0, 0, 0))
        self.add_field(f"Updated", f"<t:{int(now.timestamp())}:R>")