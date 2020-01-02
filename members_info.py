from datetime import datetime


class MembersInfo:

    def __init__(self, member_name, member_status, member_activity):
        self.member_name = f'{member_name}'
        self.member_status = f'{member_status}'
        if f'{member_activity}'.startswith('<'):
            self.member_activity = 'Custom Status'
        else:
            self.member_activity = f'{member_activity}'
        self.now_time = int(datetime.timestamp())
