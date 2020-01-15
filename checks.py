from discord.ext import commands


def is_azure():
    async def predicate(ctx):
        return ctx.author.id == 337437436680339457
    return commands.check(predicate)
