# Main bot file, starts the bot and everything else from here
import os

from discord.ext import commands

from database_sqlite import *

# The prefix of the commands that the bot uses
client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    """
    Whenever the bot is loaded and ready for action, it writes to the console.
    Checks if the databases and tables inside of it exist, and if they don't, calls functions to create them.
    :return:
    """
    print("Bot is ready")
    create_members_info_table()
    print("Members Table is ready")
    create_activities_table()
    print("Activities Table is ready")
    create_statuses_table()
    print("Statuses Table is ready")


# @client.event
# async def on_error(event, *args, **kwargs):
#    message = args[0]
#    print(traceback.format_exc())


@client.command()
async def load(ctx, extension):
    """
    Load the cogs.
    :param ctx:
    :param extension:
    :return:
    """
    client.load_extension(f'cogs.{extension}')


# Command to unload cogs
@client.command()
async def unload(ctx, extension):
    """
    Unload the cogs.
    :param ctx:
    :param extension:
    :return:
    """
    client.unload_extension(f'cogs.{extension}')


# Command to reload cogs
@client.command()
async def reload(ctx, extension):
    """
    Reload all cogs.
    :param ctx:
    :param extension:
    :return:
    """
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


# Load all the cogs from the files in the cogs folder on startup of bot.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# The token provided by Discord Application in order to authenticate the bot (Required in order to connect the bot
# to the Discord servers).
client.run('')
