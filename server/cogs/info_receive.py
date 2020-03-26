from discord.ext import commands, tasks
from server.database.members_info import MembersInfo
import sqlite3
from server.database.database_sqlite import DATABASE_DIRECTORY
from datetime import datetime


class InfoReceive(commands.Cog):
    """
    Receives info from Discord application
    """

    def __init__(self, client):
        """
        Receives and configures the Discord client for the tasks.
        :param client:
        """
        self.client = client
    members_dict = dict()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Starts the cog and starts all loop and listening tasks.
        :return:
        """
        self.get_members_list.start()
        self.get_members_db.start()
        print("Info_Receive cog is ready")

    @tasks.loop(minutes=10)
    async def get_members_list(self):
        """
        Gets all member objects from all servers tha the Bot is in and inputs them into a dictionary
        of lists with all member info.
        :return:
        """
        guilds = self.client.guilds
        all_members = []
        for guild in guilds:
            for member in guild.members:
                member_name = f'{member.name}#{member.discriminator}'
                new_member = MembersInfo(member_name, member.status, member.activity)
                all_members.append(new_member)
        for each_member in all_members:
            self.members_dict.setdefault(each_member.member_name, []).append(each_member)

    @tasks.loop(minutes=10)
    async def get_members_db(self):
        """
        Receives all members from all discord servers that the Bot is in every X time and
        inputs them into the members.db database.
        :return:
        """
        try:
            guilds = self.client.guilds
            all_members = []
            for guild in guilds:
                for member in guild.members:
                    member_name = f'{member.name}#{member.discriminator}'
                    new_member = MembersInfo(member_name, member.status, member.activity)
                    all_members.append(new_member)
            unique_members = []
            for mem in all_members:
                if all(map(lambda un_mem: un_mem.member_name != mem.member_name, unique_members)):
                    unique_members.append(mem)

            # Enter info into database
            conn = sqlite3.connect(DATABASE_DIRECTORY)
            c = conn.cursor()
            for u_mem in unique_members:
                # If there are new activities, insert them into the database
                c.execute("SELECT act_name FROM activities")
                activities_old = c.fetchall()
                is_in = False
                for act in activities_old:
                    if u_mem.member_activity == act[0]:
                        is_in = True
                        break
                if not is_in:
                    c.execute("INSERT INTO activities(id, act_name) VALUES (?, ?)", (len(activities_old) + 1,
                                                                                     str(u_mem.member_activity),))
                conn.commit()

                # Takes the data from the object and inserts into database
                c.execute("SELECT id, st_name FROM statuses")
                statuses = c.fetchall()
                status_id = 0
                for status in statuses:
                    if status[1] == u_mem.member_status:
                        status_id = status[0]
                        break

                c.execute("SELECT id, act_name FROM activities")
                activities = c.fetchall()
                activity_id = 0
                for activity in activities:
                    if activity[1] == u_mem.member_activity:
                        activity_id = activity[0]
                        break

                c.execute("INSERT INTO members_info VALUES (?, ?, ?, ?)", (u_mem.member_name, u_mem.now_time, status_id,
                                                                           activity_id))
                conn.commit()
            conn.close()
            print(f'get_member_db completed || {datetime.today().strftime("%b %d %Y %H:%M")}')
        except Exception as e:
            print(str(e))


def setup(client):
    """
    Adds current file into cog list.
    :param client:
    :return:
    """
    client.add_cog(InfoReceive(client))
