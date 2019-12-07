# This cog handles all the errors that occur.
from discord.ext import commands
from cogs.Example import Example


class Errors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Errors cog is ready")

    # If any error happens it sends it to this function which either sends a message back to the user or displays
    # the error in the console.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Error for command that does not exist. Sends back message to user.
        if isinstance(error, commands.CommandNotFound):
            print('')
            print(f'Error: CommandNotFound')
            await ctx.send(f'The command you tried to use does not exist, for a list of all available'
                           f' commands please type __**.help**__ ')
        # Any other error not specified. Raises the command in console.
        else:
            print(f'Error: {error}')

    # Errors for clear command
    @Example.clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print('')
            print(f'Error: clear- MissingArgument')
            await ctx.send(f'Please specify an amount of messages to delete.')
        elif isinstance(error, commands.BadArgument):
            print('')
            print(f'Error: clear- BadArgument')
            await ctx.send(f'Please only enter a **number** of messages to delete, not letters or symbols, etc...')

    # Errors for _8ball command
    @Example._8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print('')
            print(f'Error: _8ball- MissingArgument')
            await ctx.send(f'Please specify the question you want to ask the magical 8ball.')

    @Example.kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print('')
            print(f'Error: kick- MissingArgument')
            await ctx.send(f'Please specify and **mention (@)** the member you would like to kick.')
        elif isinstance(error, commands.BadArgument):
            print('')
            print(f'Error: kick- BadArgument')
            await ctx.send(f'The member you tried to kick does not exist. Please make sure you are **mentioning**'
                           f' **(@)** a member that is part of this discord server.')

    @Example.ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print('')
            print(f'Error: ban- MissingArgument')
            await ctx.send(f'Please specify and **mention (@)** the member you would like to ban.')
        elif isinstance(error, commands.BadArgument):
            print('')
            print(f'Error: ban- BadArgument')
            await ctx.send(f'The member you tried to ban does not exist. Please make sure you are **mentioning**'
                           f' **(@)** a member that is part of this discord server.')

    @Example.unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print('')
            print(f'Error: unban- MissingArgument')
            await ctx.send(f'Please specify the user you would like to unban.')
        elif isinstance(error, commands.BadArgument):
            print('')
            print(f'Error: kick- BadArgument')
            await ctx.send(f'Either the member is not banned, or the name of the user you entered is not correct, '
                           f'make sure you specify a user that is banned and that you entered the right name.')



def setup(client):
    client.add_cog(Errors(client))
