import json
import requests
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
from lxml import html


class UpdateChecker(commands.Cog):
    """
    Update Checking Extension
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.azure_id = 337437436680339457
        self.started = False
        self.message = ""
        print(f'Cog "{self.qualified_name}" loaded!')

    def start_loop(self):
        # Start updater loop
        if self.started is False:
            self.updater_loop.start()
            self.started = True

    def cog_unload(self):
        self.updater_loop.cancel()

    @commands.command()
    async def checkUpdateLoop(self, ctx):
        reply = f"UpdateLoop running status: {self.started}"
        reply += f"\n - Latest Firefox: {self.config['UpdateChecker']['firefox_latest']}"
        reply += f"\n - Latest Chrome: {self.config['UpdateChecker']['chrome_latest']}"
        reply += f"\n - Latest Office: {self.config['UpdateChecker']['office_latest']}"
        reply += f"\n - Latest Windows: {self.config['UpdateChecker']['office_latest']}"
        await ctx.send(reply)


    @tasks.loop(seconds=5.0)
    async def updater_loop(self):
        """Main loop to check for software updates."""

        # Check Firefox
        await self.u_getFirefoxVersion()

        # Check Chrome
        await self.u_getChromeVersion()

        # Check Office
        await self.u_getOfficeVersion()

        # Check Windows
        await self.u_getWindowsVersions()

        # If there's contents, send in one digest
        if self.message != "":
            azure = await self.bot.fetch_user(self.azure_id)
            await azure.dm_channel.send(self.message)
            self.message = ""

    async def u_getFirefoxVersion(self):
        """ Function to check for Firefox updates. """

        # Get Release Notes Page
        page = requests.get('https://www.mozilla.org/en-US/firefox/notes/').content
        pagedata = BeautifulSoup(page, "html.parser")
        version = pagedata.find('div', class_='c-release-version').text

        # Check against saved version
        if version != self.config['UpdateChecker']['firefox_latest']:
            print("Firefox update detected!")
            self.message += f"Firefox update detected! New version {version} released!\n"
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
            self.message += f"Chrome update detected! New version {version} released!\n"
            self.config['UpdateChecker']['chrome_latest'] = version
            self.u_saveConfig()

    async def u_getOfficeVersion(self):
        """ Function to check for Microsoft Office updates """

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
            self.message += f"Office update detected! New version {version} released!\n"
            self.config['UpdateChecker']['office_latest'] = version
            self.u_saveConfig()

    async def u_getWindowsVersions(self):
        """ Function to check for Microsoft Windows 1909/1809-LTSC updates """

        # Get Release Notes Page
        page = requests.get('https://winreleaseinfoprod.blob.core.windows.net/winreleaseinfoprod/en-US.html').content
        root = html.fromstring(page)

        # For some reason, lxml tosses out <tbody> elements when parsing. odd.
        for i in range(len(root.xpath("/html/body/div/table[1]")[0]) - 2):
            release_num = root.xpath(f"/html/body/div/table[1]/tr[{i+2}]/td[1]")[0].text_content()
            if release_num == "1909":
                build_1909 = root.xpath(f"/html/body/div/table[1]/tr[{i+2}]/td[4]")[0].text_content()
                # kb_article_1909 = root.xpath(f"/html/body/div/table[3]/tr[{i+2}]/td[4]")[0].text_content()
            elif release_num == "1809":
                build_1809 = root.xpath(f"/html/body/div/table[1]/tr[{i+2}]/td[4]")[0].text_content()
                # kb_article_1809 = root.xpath(f"/html/body/div/table[3]/tr[2]/td[4]")[0].text_content()

        # Check against saved versions
        if build_1909 != self.config['UpdateChecker']['windows_1909_latest']:
            print("Windows 1909 update detected!")
            self.message += f"Windows 1909 update detected! New build {build_1909} released!\n"
            self.config['UpdateChecker']['windows_1909_latest'] = build_1909
            self.u_saveConfig()
        if build_1809 != self.config['UpdateChecker']['windows_1809_latest']:
            print("Windows 1809 update detected!")
            self.message += f"Windows 1809 update detected! New build {build_1809} released!\n"
            self.config['UpdateChecker']['windows_1809_latest'] = build_1809
            self.u_saveConfig()

    def u_saveConfig(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


def setup(bot):
    bot.add_cog(UpdateChecker(bot))
