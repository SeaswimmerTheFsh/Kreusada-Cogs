import discord

from redbot.core import commands, Config

class Awaken(commands.Cog):
    """
    Bot? [botname]?

    Invoke the ping command by asking if your bot is there.
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 32482347932, force_registration=True)
        self.config.register_global(botname=None)

    @commands.group()
    async def awaken(self, ctx):
        """Commands to configure awakening."""

    @awaken.command(name="set")
    @commands.is_owner()
    async def _set(self, ctx, botname: str):
        """
        Set the bot name to listen for.

        Example Input:
        `[p]awakenset walle`
        `[p]awakenset r2d2`
        `[p]awakenset [botname]`

        Usage:
        When you type [botname]?, or whatever you configure your name as,
        it will invoke the ping command.
        
        NOTE: Do not include the question mark.
        """
        await self.config.botname.set(botname)
        await ctx.send(f"{ctx.me.name} will now invoke the ping command when it hears `{botname}?`.")

    @awaken.command()
    async def reset(self, ctx):
        """Reset and disable Awaken."""
        await ctx.tick()
        await self.config.botname.set(None)

    @awaken.command()
    @commands.is_owner()
    async def settings(self, ctx):
        """Show the current settings for Awaken."""
        botname = await self.config.botname()
        if botname:
            await ctx.send(f"{ctx.me.name} will respond to `{botname}?`.")
        else:
            await ctx.send("A name has not been set.")

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        defa = await self.config.botname()
        if defa:
            defa = defa.strip('?')
        else:
            return
        if not message.guild:
            return
        if message.author.bot:
            return
        if message.content.startswith(defa) and message.content.endswith('?'):
            ctx = await self.bot.get_context(message)
            return await ctx.invoke(self.bot.get_command('ping'))

