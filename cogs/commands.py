from discord.ext import commands
from checks import is_azure
from discord import Game


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        print(f'Cog "{self.qualified_name}" loaded!')

    @commands.command()
    @is_azure()
    async def status(self, ctx, *, new_status):
        new_game = Game(name=new_status)
        await self.bot.change_presence(activity=new_game)
        self.config['AzureBot']['Status'] = new_status


def setup(bot):
    bot.add_cog(Commands(bot))
