import discord
from discord.ext import commands, tasks
from itertools import cycle
import random


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

    # When member joins server, it writes that in terminal
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print('')
        print(f'{member} has joined a server')

    # When member leaves server, it writes that in terminal
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print('')
        print(f'{member} has left a server')

    # Command which let's user request ping and returns the ping in chat
    # @commands.command()
    # async def ping(ctx):
    #     await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

    # Command which lets user ask a question and then generates a random response
    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Yes.',
                     'Ask again later.',
                     'My sources say no.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    # Command to clear chat of (X) amount of messages
    @commands.command()
    async def clear(self,  ctx, amount: int):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)

    # Command to kick users
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for {reason}')

    # Command to ban users
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for {reason}')

    # Command to unban users
    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return


def setup(client):
    client.add_cog(Example(client))
