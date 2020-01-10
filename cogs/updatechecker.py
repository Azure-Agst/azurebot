import json
import requests
from discord.ext import tasks, commands
from bs4 import BeautifulSoup


class UpdateChecker(commands.Cog):
    """
    Update Checking Extension
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.azure_id = 337437436680339457
        print(f'Cog "{self.qualified_name}" loaded!')

        # Start updater loop
        self.updater_loop.start()

    def cog_unload(self):
        self.updater_loop.cancel()

    @tasks.loop(seconds=5.0)
    async def updater_loop(self):
        """Main loop to check for software updates."""

        # Check Firefox
        await self.u_getFirefoxVersion()

        # Check Chrome
        await self.u_getChromeVersion()

        # Check Office
        await self.u_getOfficeVersion()


    async def u_getFirefoxVersion(self):
        """ Function to check for Firefox updates. """

        # Get Release Notes Page
        page = requests.get('https://www.mozilla.org/en-US/firefox/notes/').content
        pagedata = BeautifulSoup(page, "html.parser")
        version = pagedata.find('div', class_='c-release-version').text

        # Check against saved version
        if version != self.config['UpdateChecker']['firefox_latest']:
            print("Firefox update detected!")
            azure = await self.fetch_user(self.azure_id)
            await azure.dm_channel.send(f"Firefox update detected! New version {version} released!")
            self.config['UpdateChecker']['firefox_latest'] = version
            self.u_saveConfig()

    async def u_getChromeVersion(self):
        """ Function to check for Google Chrome updates. """

        # Get Release Notes Page
        page = requests.get('https://omahaproxy.appspot.com/json').content
        data = json.loads(page)
        for i in range(len(data)):
            if data[i]["os"] == "mac":
                platform = data[i]['versions']
                for j in range(len(platform)):
                    if platform[j]["channel"] == "stable":
                        version = platform[j]['version']

        # Check against saved version
        if version != self.config['UpdateChecker']['chrome_latest']:
            print("Chrome update detected!")
            azure = await self.fetch_user(self.azure_id)
            await azure.dm_channel.send(f"Chrome update detected! New version {version} released!")
            self.config['UpdateChecker']['chrome_latest'] = version
            self.u_saveConfig()

    async def u_getOfficeVersion(self):
        """ Function to check for Office updates """
        page = requests.get('https://macadmins.software/latest.xml').content
        pagedata = BeautifulSoup(page, "xml")
        id_arr = pagedata.find_all('id')
        version_arr = pagedata.find_all('version')
        for i in range(len(id_arr)):
            if id_arr[i].get_text() == "com.microsoft.office.suite.2016":
                version = version_arr[i].get_text()

        # Check against saved version
        if version != self.config['UpdateChecker']['office_latest']:
            print("Office update detected!")
            azure = await self.fetch_user(self.azure_id)
            await azure.dm_channel.send(f"Office update detected! New version {version} released!")
            self.config['UpdateChecker']['office_latest'] = version
            self.u_saveConfig()

    def u_saveConfig(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


def setup(bot):
    bot.add_cog(UpdateChecker(bot))
