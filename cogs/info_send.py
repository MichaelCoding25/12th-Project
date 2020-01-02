from discord.ext import commands
from cogs.info_receive import InfoReceive


class InfoSend(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info_Send cog is ready")
        print('')

    @commands.command()
    async def member_last_status(self, ctx, status, *, member):
        if not status == 'online' and not status == 'idle' and not status == 'dnd' and not status == 'do_not_disturb'\
                and not status == 'offline':
            await ctx.send(f'`{status}` is not an acceptable parameter, please try any of these for the'
                           f' status parameter: `online` `do_not_disturb` `idle` `offline`')
            return
        if status == 'do_not_disturb':
            status = 'dnd'
        for instance in reversed(InfoReceive.members_dict[member]):
            if instance.member_status == f'{status}':
                if status == 'dnd':
                    await ctx.send(f"`{member} was last on Do Not Disturb on {instance.now_datetime} `")
                    return
                else:
                    await ctx.send(f"`{member} was last {status} on {instance.now_datetime} `")
                    return

        if status == 'dnd':
            await ctx.send(f'I am sorry but it seems that I was not able to find that `{member}`'
                           f' has ever been on `Do Not Disturb` in my life time')
        else:
            await ctx.send(f'I am sorry but it seems that I was not able to find that `{member}`'
                           f' has ever been `{status}` in my life time')

    @commands.command()
    async def member_last_activity(self, ctx, activity, *, member):
        did_find = False
        for instance in reversed(InfoReceive.members_dict[member]):
            if instance.member_activity == f'{activity}':
                await ctx.send(f"`{member}'s activity was {activity} last on {instance.now_datetime} `")
                did_find = True
                break
        if not did_find:
            await ctx.send(f'I am sorry but it seems that I was not able to find that `{member}` has ever done'
                           f' the `activity` you wanted to check in my life time.')


def setup(client):
    client.add_cog(InfoSend(client))
