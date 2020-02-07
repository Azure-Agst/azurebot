import configparser
from os import path
from discord import Game
from discord.ext import tasks, commands
from datetime import datetime
from os import walk


azure_id = 337437436680339457
dev = False


class AzureBot(commands.Bot):
    """The main bot!"""

    def __init__(self, command_prefix, description):
        super().__init__(command_prefix=command_prefix, description=description)

        print("#######################")
        print("#     AzureBot.py     #")
        print("# (c) 2019 Azure-Agst #")
        print("#######################")
        print()

        # read config
        self.config = configparser.ConfigParser()
        if path.exists("config.ini"):
            self.config.read('config.ini')
        else:
            self.config['AzureBot'] = {}
            self.config['AzureBot']['Status'] = "python 2 is dead!!"
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

        # get startup time
        self.startup = datetime.now()

        # for extensions
        self.failed_cogs = []

        # start autosave
        self.save_loop.start()


    def load_cogs(self):
        print("Loading Cogs...")
        (_, _, cogfiles) = next(walk("cogs"))
        for cog in cogfiles:
            ext = "cogs." + cog.split(".")[0]
            try:
                self.load_extension(ext)
            except BaseException as e:
                self.failed_cogs.append([ext, type(e).__name__, e])
        print("Done!\n")

    async def on_ready(self):
        print(f'We have logged in as {self.user}\n')

        # set startup status
        activity = Game(name=self.config['AzureBot']['Status'])
        await self.change_presence(activity=activity)

        # its me!
        azure = await self.fetch_user(azure_id)
        if azure.dm_channel is None:
            await azure.create_dm()
        if not dev:
            await azure.dm_channel.send(f"Azurebot started at {datetime.now()}")

        # start all loops
        print("Starting loops...")
        for cogname in self.cogs:
            cog = self.get_cog(cogname)
            if hasattr(cog, 'start_loop'):
                cog.start_loop()
                print(f"{cog.__class__.__name__}'s loop has started!")
        print("Done!\n")


        # display failed cogs
        if len(self.failed_cogs) != 0:
            print("Some addons failed to load:")
            for f in self.failed_cogs:
                print("{}: `{}: {}`".format(*f))
            print()

    @tasks.loop(seconds=60)
    async def save_loop(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


# run it
def main():
    try:
        bot = AzureBot("a!", "Azure's Custom Bot!")
        bot.load_cogs()
        bot.run(open("key.txt", "r").read())
        return 0
    except:
        t, v, tb  = sys.exc_info()
        print(f"Error: {t}, {v}\nFrame: {tb.tb_frame}")
        return 1


if __name__ == '__main__':
    exit(main())
