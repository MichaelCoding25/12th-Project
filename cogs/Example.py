import discord
from discord.ext import commands, tasks
from itertools import cycle


status = cycle(['Status 1', 'Status 2'])


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('with code.'))
        self.change_status.start()
        print("Bot is ready")

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @tasks.loop(seconds=1)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))


def setup(client):
    client.add_cog(Example(client))
