from libs import DB


class TimeCalc:
    def __init__(self, config):
        self.config = config
        self.db = DB.DB(self.config)

    def get_join_list(self):
        return self.db.getData(
            "SELECT `voice_id`, `user_id`, `datetime` FROM `voice_time` WHERE `type` = 'join' AND `deleted` = 0;"
        )

    def get_leave(self, voice_id, user_id, datetime):
        result = self.db.getData(
            f"SELECT `datetime` FROM `voice_time` WHERE `type` = 'leave' AND `deleted` = 0 AND `voice_id` = '{voice_id}' AND `user_id` = '{user_id}' AND  `datetime` >= {datetime};"
        )

        if not result:
            return [{'datetime': datetime}]

        return result

    def get_first_timestamp(self):
        return self.db.getData(
            f"SELECT `datetime` FROM `voice_time` WHERE `id` = 1 AND `deleted` = 0;"
        )

    def get_join_list_time(self):
        join_list = self.get_join_list()

        result = dict()
        for item in join_list:
            join_time = item['datetime']
            leave_time = self.get_leave(item['voice_id'], item['user_id'], item['datetime'])[0]['datetime']

            if item['user_id'] not in result:
                result[item['user_id']] = 0

            result[item['user_id']] += leave_time - join_time

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
