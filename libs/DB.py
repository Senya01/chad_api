import pymysql.cursors


class DB:
    def __init__(self, config):
        self.config = config

    def connection(self):
        return pymysql.connect(
            host=self.config['database']['host'],
            user=self.config['database']['user'],
            password=self.config['database']['password'],
            database=self.config['database']['database'],
            cursorclass=pymysql.cursors.DictCursor
        )

    def getData(self, sql):
        connection = self.connection()

        with connection:
            with connection.cursor() as cursor:
                # %s
                # data - (some1, some2)
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
