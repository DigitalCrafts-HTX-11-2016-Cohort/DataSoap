# coding=utf-8
import settings as settings
import datetime
if settings.local:
    import pymsgbox
# if not settings.local:
    # import gi
    # gi.require_version("Gtk", "3.0")
    # from gi.repository import Gtk
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
            else:
                return True
        except ValueError:
            return False

    @staticmethod
    def popup(message):
        if settings.local:
            pymsgbox.alert(text=message, title='Alert', button='OK')
        else:
            # window = Gtk.Window(title="Alert")
            # # label = Gtk.Label(message)
            # window.show()
            # window.connect("delete-event", Gtk.main_quit)
            # Gtk.main()
            pass