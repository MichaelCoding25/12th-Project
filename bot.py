# bot.py
import os
import random

import discord
from discord.ext import commands

# The prefix of the commands that the bot uses
client = commands.Bot(command_prefix='.')


# Whenever the bot is loaded and ready for action, it writes to the console
# @client.event
# async def on_ready():
#     print("Bot is ready")


# When member joins server, it writes that in terminal
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')


# When member leaves server, it writes that in terminal
@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')


# Command which let's user request ping and returns the ping in chat
# @client.command()
# async def ping(ctx):
#     await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Command which lets user ask a question and then generates a random response
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Yes.',
                 'Ask again later.',
                 'My sources say no.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# Command to clear chat of (X) amount of messages
@client.command()
async def clear(ctx, amount=5):
    amount = amount + 1
    await ctx.channel.purge(limit=amount)


# Command to kick users
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention} for {reason}')


# Command to ban users
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} for {reason}')


# Command to unban users
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


# Command to load cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


# Command to unload cogs
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


# Load all the cogs from the files in the cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NjI0MTg1MzgyMjM3MzcyNDIx.Xb6WZA.J38Me0N_LMlfQ0Kre1j9I_KpMKY')
