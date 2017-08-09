# coding=utf-8
import settings as settings
import datetime
from flask import request


# noinspection PyTypeChecker
class Database:
    @staticmethod
    def debug(line):
        if settings.local:
            target = open("static/debug.log", "a")
        else:
            target = open("/var/www/FlaskApp/DNCApp/debug.log", "a")
        ip = request.remote_addr
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%f")
        target.write("\n[%s][%s] %s" % (timestamp, ip, line))
        target.close()

    @staticmethod
    def escape(value):
        return value.replace("'", "''")

    @staticmethod
    def getConnection():
        return settings.connection

    @staticmethod
    def getResult(query, getOne=False):
        """Return a tuple of results or a single item (not in a tuple)
        """
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        if getOne:
            result_initial = cur.fetchall()
            try:
                result_set = result_initial[0]
            except:
                result_set = result_initial
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
    def is_phone(data):
        # Database.debug("In Database.is_phone function")
        try:
            int(Database.scrub(data))
            data_i = Database.scrub(data)
            if data_i[0] == "1":
                return False
            elif data_i[1] == "9":
                return False
            elif data_i[1] == data_i[2]:
                return False
            elif data_i[:2] == "37":
                return False
            elif data_i[:2] == "96":
                return False
            elif len(data_i) != 10:
                return False
            else:
                return True
        except ValueError:
            return False


# class DialogExample(Gtk.Dialog):
#
#     def __init__(self, parent):
#         Gtk.Dialog.__init__(self, "Alert", parent, 0,
#             (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
#              Gtk.STOCK_OK, Gtk.ResponseType.OK))
#
#         self.set_default_size(150, 100)
#
#         label = Gtk.Label("This is a dialog to display additional information")
#
#         box = self.get_content_area()
#         box.add(label)
#         self.show_all()