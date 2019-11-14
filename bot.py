# bot.py
import os

import discord
from discord.ext import commands

# The prefix of the commands that the bot uses
client = commands.Bot(command_prefix='.')


# Whenever the bot is loaded and ready for action, it writes to the console
# @client.event
# async def on_ready():
#     print("Bot is ready")


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

client.run('placeholder')
