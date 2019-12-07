from discord.ext import commands, tasks
from members_info import MembersInfo


class InfoReceive(commands.Cog):

    def __init__(self, client):
        self.client = client
    members_dict = dict()

    @commands.Cog.listener()
    async def on_ready(self):
        self.get_members.start()
        print("Info_Receive cog is ready")

    @tasks.loop(seconds=5)
    async def get_members(self):
        guilds = self.client.guilds
        all_members = []
        for guild in guilds:
            for member in guild.members:
                member_name = f'{member.name}#{member.discriminator}'
                new_member = MembersInfo(member_name, member.guild, member.status, member.activity)
                all_members.append(new_member)
        for each_member in all_members:
            self.members_dict.setdefault(each_member.member_name, []).append(each_member)


def setup(client):
    client.add_cog(InfoReceive(client))
