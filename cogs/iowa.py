import json
import requests
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
from lxml import html


class Iowa(commands.Cog):
    """
    Update Checking Extension
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.azure_id = 337437436680339457
        self.started = False
        self.config['iowa'] = {}
        print(f'Cog "{self.qualified_name}" loaded!')
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def start_loop(self):
        # Start updater loop
        if self.started is False:
            self.iowa_loop.start()
            self.started = True

    def cog_unload(self):
        self.iowa_loop.cancel()

    @commands.command()
    async def checkIowaLoop(self, ctx):
        """View Iowa loop/Get current versions."""
        reply = f"UpdateLoop running status: {self.started}"
        reply += f"\n - Latest Update: {self.config['iowa']['latest_percent']}"
        await ctx.send(reply)


    @tasks.loop(seconds=15.0)
    async def iowa_loop(self):
        """Main loop to check for iowa updates."""

        # Get Release Notes Page
        page = requests.get('https://results.thecaucuses.org/').content
        root = html.fromstring(page)
        reported = root.xpath("/html/body/div/div/div/div[1]")[0].text_content()
        percent = reported.split(' ')[0]

        if percent != self.config['iowa']['latest_percent']:
            self.config['iowa']['latest_percent'] = percent
            azure = await self.bot.fetch_user(self.azure_id)
            await azure.dm_channel.send(f"Iowa results updated to {percent}%\nhttps://results.thecaucuses.org/")
            self.u_saveConfig()

    def u_saveConfig(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


def setup(bot):
    bot.add_cog(Iowa(bot))
