import re
import sqlite3
from datetime import datetime

import discord
from discord.ext import commands

import server.graphs.graph_creation as gc
from server.database.database_sqlite import MEMBERS_DATABASE_DIRECTORY
from server.graphs.graph_creation import GRAPHS_DIRECTORY


def member_security_check(ctx, member: str):
    for mem in ctx.guild.members:
        if re.search('[a-zA-Z]', member):
            if member == str(mem.name + '#' + mem.discriminator):
                return True
        else:
            if member == str(mem.id):
                return True

    return False


class StatCommands(commands.Cog):
    """
    User statistics commands.
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
        print("StatCommands cog is ready")
        print('')

    @commands.command(pass_context=True)
    async def member_last_stat(self, ctx, stat_type, stat_name, *, member):
        """

        """
        return_msg = ''

        if member_security_check(ctx, member):
            if str(stat_type).lower() == 'status':
                return_msg = self.member_last_status(ctx, stat_name, member)
            elif str(stat_type).lower() == 'activity':
                return_msg = self.member_last_activity(ctx, stat_name, member)
        else:
            return_msg = f"{member} is not currently in your server. If you would like to check his information " \
                         f"please make sure he is a part of your Discord server."

        await ctx.send(return_msg)

    def member_last_status(self, ctx, status, member):
        member_name = member.name + '#' + member.discriminator
        statuses = {'online', 'idle', 'dnd', 'do not disturb', 'offline'}
        if status not in statuses:
            return f'`{status}` is not an acceptable parameter, please try any of these for the status parameter: ' \
                   f'`online` `do_not_disturb` `idle` `offline` '
        if status == 'do_not_disturb':
            status = 'dnd'
        conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
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
            return f'`I am sorry but it seems that I was not able to find that `{member}` has ever been `{status}`' \
                   f' in my database.` '

    def member_last_activity(self, ctx, activity, member):
        member_name = member.name + '#' + member.discriminator
        if member_security_check(ctx, member):
            if re.search('[a-zA-Z]', str(member)):
                discord_member = ctx.guild.get_member_named(member)
            else:
                discord_member = ctx.guild.get_member(int(member))
        else:
            # await ctx.send(f"{ctx.message.author.mention} {member_name} is not currently in your server. If you
            # would like to check his information please make sure he is a part of your Discord server.")
            return
        conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
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
            return f"`{ctx.message.author.mention} Unfortunately I was not able to find the **activity** you are " \
                   f"looking for, please try entering one of these activities: **{activities_list}**.` "

        c.execute("SELECT * FROM activities")
        activities = c.fetchall()
        c.execute("SELECT * FROM members_info WHERE mem_id = ? OR mem_id = ?", (member.id, member_name))
        instances = c.fetchall()
        c.close()

        for act in activities:
            if str(act[1]).lower() == str(activity).lower():
                activity_id = act[0]

        for instance in reversed(instances):
            if instance[3] == activity_id:
                return f"`{member_name} was last {activity} at " \
                       f"{datetime.fromtimestamp(instance[1]).strftime('%Y-%m-%d %H:%M:%S')}`"

        return f'`Unfortunately I was not able to find in my database that {member_name} has ever done {activity}`'

    @commands.command(pass_context=True)
    async def get_user_stats(self, ctx, stat_type, num_of_days, graph_type, display_public, *, member):
        if int(num_of_days) > 20:
            await ctx.send(f"{ctx.message.author.mention} You may only request data that is 20 days old, or less. "
                           f"Please try again.")
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

        if member_security_check(ctx, member):
            if re.search('[a-zA-Z]', str(member)):
                discord_member = ctx.guild.get_member_named(member)
            else:
                discord_member = ctx.guild.get_member(int(member))

            if str(graph_type).lower() == 'bar' or str(graph_type).lower() == 'pie':
                if str(stat_type).lower() == 'statuses':
                    return_msg, return_img = self.get_user_statuses(ctx, num_of_days, graph_type, discord_member)
                elif str(stat_type).lower() == 'activities':
                    return_msg, return_img = self.get_user_activities(ctx, num_of_days, graph_type, discord_member)
                else:
                    return await ctx.send(f"{ctx.message.author.mention} ```css\n [ERROR] You failed to provide a valid"
                                          f" parameter for stat_type, try again with one of the following:"
                                          f" statuses / activities.```")
            else:
                return await ctx.send(f"{ctx.message.author.mention} ```css\n [ERROR] You failed to provide a valid "
                                      f"graph type, try again with one of the following: pie /  bar.```")

            return_embed.description = return_msg
            return_embed.set_image(url=f"attachment://{return_img.filename}")
            if str(display_public).lower() == 'yes':
                await ctx.send(embed=return_embed, file=return_img)
            elif str(display_public).lower() == 'no':
                await ctx.message.author.send(embed=return_embed, file=return_img)
            else:
                return await ctx.send(f"{ctx.message.author.mention} ```css\n [ERROR] You failed to provide a valid "
                               f"parameter for display_public, try again with one of the following: Yes / No.```")
        else:
            return await ctx.send(f"{ctx.message.author.mention} ```css\n [ERROR] {member} is not currently in "
                                  f"your server. If you would like to check his information, please make"
                                  f" sure he is a part of this Discord server.```")

    def get_user_statuses(self, ctx, num_of_days, graph_type, member: discord.Member):
        member_name = member.name + '#' + member.discriminator
        if graph_type == 'pie':
            db_conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'

            cursor.execute("SELECT status_id FROM members_info WHERE (mem_id = ? AND date_time >="
                           "strftime('%s',datetime('now',?))) OR (mem_id = ? AND date_time >=strftime"
                           "('%s',datetime('now',?)))", (member.id, days_string, member_name, days_string))
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

            return_img = discord.File(f"{GRAPHS_DIRECTORY}/status_pie_graph.png", filename="status_pie_graph.png")
            return_message = f"Graph of {member_name}'s statuses from the last {num_of_days}d.\nRequested by" \
                             f" {ctx.message.author.mention}"

        elif graph_type == 'bar':
            db_conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'
            cursor.execute("SELECT status_id, date_time FROM members_info WHERE (mem_id = ? AND date_time >="
                           "strftime('%s',datetime('now',?))) OR (mem_id = ? AND date_time >=strftime"
                           "('%s',datetime('now',?)))", (member.id, days_string, member_name, days_string))
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
            return_message = f"Graph of {member_name}'s statuses from the last {num_of_days}d per day.\nRequested by" \
                             f" {ctx.message.author.mention}"
            img.close()

        return return_message, return_img

    def get_user_activities(self, ctx, num_of_days, graph_type, member: discord.Member):
        member_name = member.name + '#' + member.discriminator
        if graph_type == 'pie':
            db_conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'

            cursor.execute("SELECT activity_id FROM members_info WHERE (mem_id = ? AND date_time >="
                           "strftime('%s',datetime('now',?))) OR (mem_id = ? AND date_time >=strftime"
                           "('%s',datetime('now',?)))", (member.id, days_string, member_name, days_string))
            activity_ids = cursor.fetchall()
            cursor.execute("SELECT * FROM activities")
            all_activities_db = cursor.fetchall()
            db_conn.close()

            all_activities = []
            for activity_id in activity_ids:
                for act in all_activities_db:
                    if act[0] == activity_id[0]:
                        all_activities.append(act[1])

            activities_names = []
            for activity in all_activities_db:
                activities_names.append(activity[1])

            gc.create_activity_pie_graph(all_activities, activities_names)

            return_img = discord.File(f"{GRAPHS_DIRECTORY}/activity_pie_graph.png", filename="activity_pie_graph.png")
            return_message = f"Graph of {member_name}'s activities from the last {num_of_days}d.\nRequested by" \
                             f" {ctx.message.author.mention}"

        elif graph_type == 'bar':
            db_conn = sqlite3.connect(MEMBERS_DATABASE_DIRECTORY)
            cursor = db_conn.cursor()
            days_string = f'-{num_of_days} days'
            cursor.execute("SELECT activity_id, date_time FROM members_info WHERE (mem_id = ? AND date_time >="
                           "strftime('%s',datetime('now',?))) OR (mem_id = ? AND date_time >=strftime"
                           "('%s',datetime('now',?)))", (member.id, days_string, member_name, days_string))
            activities = cursor.fetchall()
            cursor.execute("SELECT * FROM activities")
            all_activities_db = cursor.fetchall()
            db_conn.close()

            day_week_activities = []
            day_in_seconds = 86400
            now = datetime.now()
            now_time = int(datetime.timestamp(now))
            for day in range(int(num_of_days)):
                day_activities = []
                for activity in activities:
                    if now_time - (day_in_seconds * (day + 1)) < activity[1] <= now_time - (day_in_seconds * day):
                        for act in all_activities_db:
                            if act[0] == activity[0]:
                                day_activities.append(act[1])
                day_week_activities.append(day_activities)

            activities_names = []
            for activity in all_activities_db:
                activities_names.append(activity[1])

            gc.create_activity_bar_graph(day_week_activities, activities_names)

            img = open(f"{GRAPHS_DIRECTORY}/activity_bar_graph.png", 'rb')
            return_img = discord.File(f"{GRAPHS_DIRECTORY}/activity_bar_graph.png", filename="activity_bar_graph.png")
            return_message = f"Graph of {member_name}'s activities from the last {num_of_days}d per day.\nRequested" \
                             f" by {ctx.message.author.mention}"
            img.close()

        return return_message, return_img


def setup(client):
    """
    Adds current class into cog list.
    :param client:
    :return:
    """
    client.add_cog(StatCommands(client))
