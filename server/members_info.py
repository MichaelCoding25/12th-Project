from datetime import datetime


class MembersInfo:

    def __init__(self, member_name, member_status, member_activity):
        """
        A class that collects all info about member and puts it into an object and adds the time the member's
        info was logged.
        :param member_name: Name and discriminator of member in question.
        :param member_status: What is the member's current status? Idle, Online, Offline or DND?
        :param member_activity: What is the member's current activity?
        """
        self.member_name = f'{member_name}'
        self.member_status = f'{member_status}'
        if 'CustomActivity' in f'{type(member_activity)}':
            self.member_activity = 'Custom Status'
        elif 'playing' in f'{member_activity}':
            self.member_activity = 'Playing'
        else:
            self.member_activity = f'{member_activity}'
        self.now = datetime.now()
        self.now_time = int(datetime.timestamp(self.now))
