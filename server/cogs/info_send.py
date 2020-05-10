import discord
from discord.ext import commands
from server.cogs.info_receive import InfoReceive
import sqlite3
import server.graphs.graph_creation as gc
from datetime import datetime
from server.database.database_sqlite import DATABASE_DIRECTORY
from server.graphs.graph_creation import GRAPHS_DIRECTORY


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
    async def member_last_stat(self, ctx, stat_type, stat_name, *, member):
        return_msg = ''

        if self.member_security_check(ctx, member):
            if str(stat_type).lower() == 'status':
                return_msg = self.member_last_status(ctx, stat_name, member)
            elif str(stat_type).lower() == 'activity':
                return_msg = self.member_last_activity(ctx, stat_name, member)
        else:
            return_msg = f"{member} is not currently in your server. If you would like to check his information " \
                         f"please make sure he is a part of your Discord server."

        await ctx.send(return_msg)

    def member_last_status(self, ctx, status, member):
        statuses = {'online', 'idle', 'dnd', 'do not disturb', 'offline'}
        if status not in statuses:
            return f'`{status}` is not an acceptable parameter, please try any of these for the status parameter: ' \
                   f'`online` `do_not_disturb` `idle` `offline` '
        if status == 'do_not_disturb':
            status = 'dnd'
        conn = sqlite3.connect(DATABASE_DIRECTORY)
        c = conn.cursor()
        c.execute("SELECT * FROM statuses")
        statuses = c.fetchall()
        c.execute("SELECT * FROM members_info WHERE mem_id = ?", (member,))
        instances = c.fetchall()
        c.close()

        for stat in statuses:
            if stat[1] == status:
                status_id = stat[0]

        for instance in reversed(instances):
            if instance[2] == status_id:
                if status == 'dnd':
                    return f"`{member} was last on Do Not Disturb at" \
                           f" {datetime.fromtimestamp(instance[1]).strftime('%Y-%m-%d %H:%M:%S')} ` "
                else:
                    return f"`{member} was last {status} at " \
                           f"{datetime.fromtimestamp(instance[1]).strftime('%Y-%m-%d %H:%M:%S')} `"

        if status == 'dnd':
            return f'`I am sorry but it seems that I was not able to find that `{member}` has ever been on `Do Not ' \
                   f'Disturb` in my database.`'
        else:
            return f'`I am sorry but it seems that I was not able to find that `{member}` has ever been `{status}` in ' \
                   f'my database.`'

    def member_last_activity(self, ctx, activity, member):
        conn = sqlite3.connect(DATABASE_DIRECTORY)
        c = conn.cursor()
        c.execute("SELECT act_name FROM activities")
        activities_tup = c.fetchall()
        is_found = False
        activities_list = []

        for act in activities_tup:
            activities_list.append(act[0])
            if str(act[0]).lower() == str(activity).lower():
                is_found = True

        if not is_found:
            c.close()
            return f"`Unfortunately I was not able to find the **activity** you are looking for, please try entering " \
                   f"one of these activities: **{activities_list}**.`"

        c.execute("SELECT * FROM activities")
        activities = c.fetchall()
        c.execute("SELECT * FROM members_info WHERE mem_id = ?", (member,))
        instances = c.fetchall()
        c.close()

        for act in activities:
            if str(act[1]).lower() == str(activity).lower():
                activity_id = act[0]

        for instance in reversed(instances):
            if instance[3] == activity_id:
                return f"`{member} was last {activity} at " \
                       f"{datetime.fromtimestamp(instance[1]).strftime('%Y-%m-%d %H:%M:%S')}`"

        return f'`Unfortunately I was not able to find in my database that {member} has ever done {activity}`'

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
        if int(num_of_days) > 20:
            await ctx.send("You may only request data that is 20 days old, or less. Please try again.")
            return
        return_msg = ''
        return_img = ''
        return_embed = discord.Embed(title='User Statistics Graph', colour=discord.Color.blue())
        return_embed.timestamp = datetime.now()

        # The member requesting the stats
        return_embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        # The member the info of is being requested
        return_embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

        return_embed.add_field(name='Statistic:', value=stat_type)
        return_embed.add_field(name='Graph Type:', value=graph_type)
        return_embed.add_field(name='Number Of Days:', value=num_of_days)

        if self.member_security_check(ctx, member):
            if str(stat_type).lower() == 'statuses':
                return_msg, return_img = self.get_user_statuses(ctx, num_of_days, graph_type, member)

            return_embed.description = return_msg
            return_embed.set_image(url=f"attachment://{return_img.filename}")
            await ctx.send(embed=return_embed, file=return_img)
        else:
            await ctx.send(f"{member} is not currently in your server. If you would like to check his information "
                           f"please make sure he is a part of your Discord server.")

    def get_user_statuses(self, ctx, num_of_days, graph_type, member):

        if graph_type == 'pie':
            db_conn = sqlite3.connect(DATABASE_DIRECTORY)
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'
            cursor.execute("SELECT status_id FROM members_info WHERE mem_id = ? AND date_time >="
                           " strftime('%s',datetime('now',?))", (member, days_string))
            status_ids = cursor.fetchall()
            cursor.execute("SELECT * FROM statuses")
            all_statuses_db = cursor.fetchall()
            db_conn.close()

            all_statuses = []
            for status_id in status_ids:
                for stat in all_statuses_db:
                    if stat[0] == status_id[0]:
                        all_statuses.append(stat[1])

            gc.create_status_pie_graph(all_statuses)

            img = open(f"{GRAPHS_DIRECTORY}/status_pie_graph.png", 'rb')
            return_img = discord.File(img)
            return_message = f"Graph of {member}'s statuses from the last {num_of_days}d.\nRequested by" \
                             f" {ctx.message.author.mention}"

        elif graph_type == 'bar':
            db_conn = sqlite3.connect(DATABASE_DIRECTORY)
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

            img = open(f"{GRAPHS_DIRECTORY}/status_bar_graph.png", 'rb')
            return_img = discord.File(f"{GRAPHS_DIRECTORY}/status_bar_graph.png", filename="status_bar_graph.png")
            return_message = f"Graph of {member}'s statuses from the last {num_of_days}d per day.\nRequested by" \
                             f" {ctx.message.author.mention}"
            img.close()

        return return_message, return_img

    def get_user_activities(self, ctx, num_of_days, graph_type, member):

        if graph_type == "pie":
            db_conn = sqlite3.connect(DATABASE_DIRECTORY)
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'
            cursor.execute("SELECT activity_id FROM members_info WHERE mem_id = ? AND date_time >="
                           " strftime('%s',datetime('now',?))", (member, days_string))
            activities_ids = cursor.fetchall()
            cursor.execute("SELECT * FROM activities")
            all_activities_db = cursor.fetchall()
            db_conn.close()

            all_activities = []
            for status_id in activities_ids:
                for stat in all_activities_db:
                    if stat[0] == status_id[0]:
                        all_activities.append(stat[1])

            act_name_list = []
            for act in all_activities_db:
                act_name_list.append(act[1])

            gc.create_status_pie_graph(all_activities, act_name_list)

            img = open(f"{GRAPHS_DIRECTORY}/activity_pie_graph.png", 'rb')
            return_img = discord.File(img)
            return_message = f"Graph of {member}'s activities from the last {num_of_days}d.\nRequested by" \
                             f" {ctx.message.author.mention}"

    def member_security_check(self, ctx, member):
        if not any(c.isalpha() for c in member):
            return True

        for mem in ctx.guild.members:
            if member == str(mem.name + '#' + mem.discriminator):
                return True

        return False


def setup(client):
    """
    Adds current class into cog list.
    :param client:
    :return:
    """
    client.add_cog(InfoSend(client))
