import discord
from discord.ext import commands
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from context_injector import ContextInjector

class Inject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.injector = ContextInjector()

    @commands.command(name="inject")
    async def inject_context(self, ctx, *, query: str):
        prompt = self.injector.inject_context(query)
        response = f"```{prompt[:1900]}```" if len(prompt) > 1900 else f"```{prompt}```"
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Inject(bot))
