# coding=utf-8
import settings as settings
# noinspection PyTypeChecker
class Database:
    @staticmethod
    def escape(value):
        return value.replace("'","''")

    @staticmethod
    def getConnection():
        return settings.connection

    @staticmethod
    def getResult(query,getOne=False):
        """Return a tuple of results or a single item (not in a tuple)
        """
        result_set=()
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        if getOne:
            result_set = cur.fetchone()
        else:
            result_set = cur.fetchall()
        cur.close()
        return result_set

    @staticmethod
    def doQuery(query):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        lastId = cur.lastrowid
        cur.close()
        return lastId

    @staticmethod
    def scrub(data):
        return filter(type(data).isdigit, data)

    @staticmethod
    def is_int(data):
        try:
            int(Database.scrub(data))
            return True
        except ValueError:
            return False

