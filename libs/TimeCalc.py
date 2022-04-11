from libs import DB


class TimeCalc:
    def __init__(self, config):
        self.config = config
        self.db = DB.DB(self.config)

    def get_users_list(self):
        return self.db.getData("SELECT DISTINCT user_id FROM voice_time WHERE `deleted` = '0';")

    # def get_join_list(self, stype=0, voice_id=0):
    #     voice_id = self.config['channels']['afk'] if voice_id == 0 else ''
    #     param = f' AND `voice_id` != {voice_id}' if stype == 0 else f' AND `voice_id` = {voice_id}'
    #
    #     return self.db.getData(
    #         f"SELECT `voice_id`, `user_id`, `datetime` FROM `voice_time` WHERE `type` = 'join' AND `deleted` = 0{param};"
    #     )

    # def get_leave(self, voice_id, user_id, datetime):
    #     result = self.db.getData(
    #         f"SELECT `datetime` FROM `voice_time` WHERE `type` = 'leave' AND `deleted` = 0 AND `voice_id` = '{voice_id}' AND `user_id` = '{user_id}' AND  `datetime` >= {datetime};"
    #     )
    #
    #     if not result:
    #         return [{'datetime': datetime}]
    #
    #     return result

    def get_first_timestamp(self):
        return self.db.getData(
            f"SELECT `datetime` FROM `voice_time` WHERE `id` = 1 AND `deleted` = 0 LIMIT 1;"
        )

    def get_time_list(self, user_id, type):
        return self.db.getData(
            f"SELECT datetime FROM voice_time WHERE deleted = '0' AND user_id = '{user_id}' AND type = '{type}';"
        )

    def get_user_info(self, user_id):
        join_list = self.get_time_list(user_id, 'join')
        leave_list = self.get_time_list(user_id, 'leave')

        i = 0
        sum = 0
        print(user_id)
        # while i < len(join_list):
        #     if i < len(leave_list):
        #         sum += leave_list[i]['datetime'] - join_list[i]['datetime']
        #         print(i, join_list[i]['datetime'], leave_list[i]['datetime'], leave_list[i]['datetime'] - join_list[i]['datetime'])
        #     i += 1
        while i < len(join_list):


            i += 1

        return sum

    def get_join_list_time(self):
        # join_list = self.get_join_list()
        users_list = self.get_users_list()

        result = dict()
        for user in users_list:
            user_id = user['user_id']

            user_info = self.get_user_info(user_id)
            result[user_id] = user_info

        # for item in join_list:
        #     join_time = item['datetime']
        #     leave_time = self.get_leave(item['voice_id'], item['user_id'], item['datetime'])[0]['datetime']
        #
        #     if item['user_id'] not in result:
        #         result[item['user_id']] = 0
        #
        #     result[item['user_id']] += leave_time - join_time

        return dict(sorted(result.items(), key=lambda y: y[1], reverse=True))

    def get_result(self, user_id):
        users = self.get_join_list_time()
        if user_id in list(users):
            place = list(users).index(user_id) + 1
            time = users[user_id]
        else:
            place = '-'
            time = 0

        return {
            'first_timestamp': self.get_first_timestamp()[0]['datetime'],
            'time': time,
            'place': place,
            'users': users
        }

    def main(self, user_id):
        return self.get_result(user_id)
