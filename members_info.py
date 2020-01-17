from datetime import datetime


class MembersInfo:

    def __init__(self, member_name, member_status, member_activity):
        self.member_name = f'{member_name}'
        self.member_status = f'{member_status}'
        if 'Custom Status' in f'{member_activity}':
            self.member_activity = 'Custom Status'
        elif 'playing' in f'{member_activity}':
            self.member_activity = 'Playing'
        else:
            self.member_activity = f'{member_activity}'
        self.now = datetime.now()
        self.now_time = int(datetime.timestamp(self.now))
