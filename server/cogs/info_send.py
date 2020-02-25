import discord
from discord.ext import commands
from cogs.info_receive import InfoReceive
import sqlite3
import graph_creation as gc
from datetime import datetime


class InfoSend(commands.Cog):
    """
    Sends data into the Discord channel chats.
    """

    def __init__(self, client):
        """
        Receives and configures the Discord client for the commands.
        :param client:
        """
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Starts the cog.
        :return:
        """
        print("Info_Send cog is ready")
        print('')

    @commands.command()
    async def member_last_status_dict(self, ctx, status, *, member):
        """
        Checks that the status the member input is correct and then searches for the last instance of that
        status in the db/dictionary and sends back to the chat the time that they had that last status.
        :param ctx: What server and channel did the command come from to be able to send it back to the right place.
        :param status: What is the status they want to receive the answer for.
        :param member: The member for which the command is being issued for.
        :return: The last time said user had that particular status.
        """
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
    async def member_last_status_db(self, ctx, status, *, member):
        statuses = {'online', 'idle', 'dnd', 'do not disturb', 'offline'}
        if status not in statuses:
            await ctx.send(f'`{status}` is not an acceptable parameter, please try any of these for the'
                           f' status parameter: `online` `do_not_disturb` `idle` `offline`')
            return
        if status == 'do_not_disturb':
            status = 'dnd'
        conn = sqlite3.connect('members.db')
        c = conn.cursor()
        c.execute("SELECT * FROM statuses")
        statuses = c.fetchall()
        c.execute("SELECT * FROM members_info WHERE mem_id = ?", (member,))
        instances = c.fetchall()

        for stat in statuses:
            if stat[1] == status:
                status_id = stat[0]

        for instance in reversed(instances):
            if instance[3] == f'{status}':
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
        c.close()

    @commands.command()
    async def member_last_activity_dict(self, ctx, activity, *, member):
        """
        Searches for the last instance of that activity in the db/dictionary and sends back to the chat
        the time that they had that last activity.
        :param ctx: What server and channel did the command come from to be able to send it back to the right place.
        :param activity: What is the activity they want to receive the answer for.
        :param member: The member for which the command is being issued for.
        :return: The last time said user was doing that particular activity.
        """
        did_find = False
        for instance in reversed(InfoReceive.members_dict[member]):
            if instance.member_activity == f'{activity}':
                await ctx.send(f"`{member}'s activity was {activity} last on {instance.now_datetime} `")
                did_find = True
                break
        if not did_find:
            await ctx.send(f'I am sorry but it seems that I was not able to find that `{member}` has ever done'
                           f' the `activity` you wanted to check in my life time.')

    @commands.command()
    async def get_user_stats(self, ctx, stat_type, num_of_days, graph_type, *, member):
        return_msg = ''
        return_img = ''

        if str(stat_type).lower() == 'status':
            return_msg, return_img = self.get_user_statuses(ctx, num_of_days, graph_type, member)

        await ctx.send(return_msg, file=return_img)


    def get_user_statuses_day(self, ctx, graph_type, member):

        db_conn = sqlite3.connect('members.db')
        cursor = db_conn.cursor()
        cursor.execute("SELECT status_id FROM members_info WHERE mem_id = ? AND date_time >="
                       " strftime('%s',datetime('now','-1 day'))", (member,))
        day_status_ids = cursor.fetchall()
        cursor.execute("SELECT * FROM statuses")
        all_statuses_db = cursor.fetchall()
        db_conn.close()

        all_day_statuses = []
        for status_id in day_status_ids:
            for stat in all_statuses_db:
                if stat[0] == status_id[0]:
                    all_day_statuses.append(stat[1])

        gc.create_status_pie_graph(all_day_statuses)

        img = open("status_pie_graph.png", 'rb')
        return_img = discord.File(img)
        return_message = f"Graph of {member}'s statuses from the last 24h.\nRequested by {ctx.message.author.mention}"

        return return_message, return_img

    def get_user_statuses(self, ctx, num_of_days, graph_type, member):

        if graph_type == 'pie':
            db_conn = sqlite3.connect('members.db')
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'
            cursor.execute("SELECT status_id FROM members_info WHERE mem_id = ? AND date_time >="
                           " strftime('%s',datetime('now',?))", (member, days_string))
            status_ids = cursor.fetchall()
            cursor.execute("SELECT * FROM statuses")
            all_statuses_db = cursor.fetchall()
            db_conn.close()

            all_week_statuses = []
            for status_id in status_ids:
                for stat in all_statuses_db:
                    if stat[0] == status_id[0]:
                        all_week_statuses.append(stat[1])

            gc.create_status_pie_graph(all_week_statuses)

            img = open("status_pie_graph.png", 'rb')
            return_img = discord.File(img)
            return_message = f"Graph of {member}'s statuses from the last {num_of_days}d.\nRequested by" \
                             f" {ctx.message.author.mention}"

        elif graph_type == 'bar':
            db_conn = sqlite3.connect('members.db')
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'
            cursor.execute("SELECT status_id, date_time FROM members_info WHERE mem_id = ? AND date_time >="
                           " strftime('%s',datetime('now',?))", (member, days_string))
            statuses = cursor.fetchall()
            cursor.execute("SELECT * FROM statuses")
            all_statuses_db = cursor.fetchall()
            db_conn.close()

            day_week_statuses = []
            day_in_seconds = 86400
            now = datetime.now()
            now_time = int(datetime.timestamp(now))
            for day in range(int(num_of_days)):
                day_statuses = []
                for status in statuses:
                    if now_time - (day_in_seconds * (day + 1)) < status[1] <= now_time - (day_in_seconds * day):
                        for stat in all_statuses_db:
                            if stat[0] == status[0]:
                                day_statuses.append(stat[1])
                day_week_statuses.append(day_statuses)

            gc.create_status_bar_graph(day_week_statuses)

            img = open("status_bar_graph.png", 'rb')
            return_img = discord.File(img)
            return_message = f"Graph of {member}'s statuses from the last {num_of_days}d per day.\nRequested by" \
                             f" {ctx.message.author.mention}"

        return return_message, return_img


def setup(client):
    """
    Adds current class into cog list.
    :param client:
    :return:
    """
    client.add_cog(InfoSend(client))
