# coding=utf-8
from database import Database
from datetime import datetime


class Users:
    def __init__(self, userid=0):
        self.firstname = ""
        self.lastname = ""
        self.company = ""
        self.email = ""
        self.username = ""
        self.password = ""
        self.id = userid

    def save(self):
        if self.id > 0:
            return self.update()
        else:
            return self.insert()

    def insert(self):
        query = ("""insert into dnc.users (firstname, lastname, company, email, username, password) 
                values ('%s','%s','%s','%s','%s',%r)"""
                 % (Database.escape(self.firstname), Database.escape(self.lastname), Database.escape(self.company),
                    Database.escape(self.email), Database.escape(self.username), self.password))
        lastID = Database.doQuery(query)
        return lastID

    def update(self):
        query = ("""update dnc.users set firstname = '%s', lastname = '%s', company = '%s', email = '%s', password = %r 
                where id = %d"""
                 % (Database.escape(self.firstname), Database.escape(self.lastname), Database.escape(self.company),
                    Database.escape(self.email), self.password, self.id))
        Database.doQuery(query)
        return True

    def acknowledge(self, fullname, company):
        query = ("""update dnc.users set date_acknowledged = '%s', name_as_typed = '%s', company_as_typed = '%s'
                where id = %d"""
                 % (datetime.now(), Database.escape(fullname), Database.escape(company), self.id))
        Database.debug(query)
        Database.doQuery(query)
        return True
