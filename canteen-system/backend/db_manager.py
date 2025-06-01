import pymysql

class DBManager:
    """数据库连接与基础操作封装"""
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="canteen_user",
                password="myRan20041118@",
                database="canteen",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
            print("数据库连接成功!")
        except pymysql.Error as err:
            print(f"数据库连接失败: {err}")
            self.conn = None
            self.cursor = None

    def execute(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            return self.cursor
        except Exception as e:
            print(f"SQL执行失败: {e}")
            return None

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()