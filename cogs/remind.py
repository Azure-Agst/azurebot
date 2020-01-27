import datetime
from discord.ext import tasks, commands


class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.azure_id = 337437436680339457
        self.target = datetime.datetime(2020, 1, 27, 6, 50)  # YY,MM,DD,HH,mm
        print(f'Cog "{self.qualified_name}" loaded!')

    def start_loop(self):
        # Start updater loop
        self.main_loop.start()

    @tasks.loop(seconds=10.0)
    async def main_loop(self):
        now = datetime.datetime.now()
        if self.config['Reminder']['reminded'] != "True" and now > self.target:
            print("Sending reminder...")

            # update config
            self.config['Reminder']['reminded'] = "True"
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

            # send user message
            user = await self.bot.fetch_user(self.config['Reminder']['target'])
            if user.dm_channel is None:
                await user.create_dm()
            await user.dm_channel.send(self.config['Reminder']['message'])

            # send ME a confirmation message
            azure = await self.bot.fetch_user(self.azure_id)
            if azure.dm_channel is None:
                await azure.create_dm()
            await azure.dm_channel.send("Sent a reminder!")


def setup(bot):
    bot.add_cog(Remind(bot))
