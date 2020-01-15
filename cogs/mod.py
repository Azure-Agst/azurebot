from subprocess import check_output
from discord.ext import commands
from checks import is_azure


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print(f'Cog "{self.qualified_name}" loaded!')

    @is_azure()
    @commands.command()
    async def reload(self, ctx):
        """Reload Bot."""
        await ctx.send("Reloading...")
        await self.bot.close()

    @is_azure()
    @commands.command()
    async def pull(self, ctx):
        """Pull new changes from GitHub and restart."""
        await ctx.send("Pulling changes...")
        output = check_output(['git', 'pull'])
        if b'Already up to date.' in output:
            await ctx.send(f"Already up to date!")
        else:
            head = check_output(["git", "log", "--pretty=format:'%h'", "-n 1"]).decode("UTF-8")
            await ctx.send(f"Updated to version {head}!\nRestarting...")
            await self.bot.close()


def setup(bot):
    bot.add_cog(Mod(bot))
