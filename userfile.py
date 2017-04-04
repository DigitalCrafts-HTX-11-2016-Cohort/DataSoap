# coding=utf-8
import settings as settings
from database import Database
import csv
import os
from flask import session, redirect


# noinspection SqlResolve
class Userfile:
    def __init__(self, filename, time_in):
        self.filename = filename
        self.path_in = settings.upload+self.filename
        self.time_in = time_in
        self.time_out = ""
        self.filename_out = self.time_in+self.filename[8:]
        self.path_out = settings.download+str(session.get('userid'))+"/"+self.filename_out
        self.phoneColList = []
        self.keep_processing = True

    def findPhoneCols(self):
        os.rename(self.path_in, ("%s.prc" % self.path_in))
        prc_file = open("%s.prc" % self.path_in)
        dReader = csv.DictReader(prc_file)
        cleanfile = open(self.path_in, "w")
        self.headers = dReader.fieldnames
        self.record_count = sum(1 for row in dReader)
        # Database.debug("Record count for uploaded userfile is:")
        # Database.debug(self.record_count)
        if self.record_count < 5:
            # Database.debug("Less than 5 rows")
            session['success_message'] = """There were not enough records in you file or you have empty rows<br />
            Please use the quick search function to scrub just a few records, or remove empty rows and try again"""
            self.keep_processing = False
            return redirect('/dashboard')
        # Database.debug("headers from old file are: %s" % self.headers)
        with open("%s.prc" % self.path_in) as prc_file:
            reader = csv.reader(prc_file)
            for i in range(5):
                row = reader.next()
                for col in row:
                    if len(Database.scrub(col)) == 10 and Database.is_int(col):
                        Database.debug("This col index should be added %d" % row.index(col))
                        if row.index(col) not in self.phoneColList:
                            self.phoneColList.append(row.index(col))
                # Database.debug(self.phoneColList)
            if not self.phoneColList:
                session['success_message'] = """There were no recognized phone number columns in you file<br />
                If you have extensions or country codes, please remove those and try again"""
                self.keep_processing = False
                return redirect('/dashboard')
            prc_file.seek(0)
            Database.debug(self.record_count)
            for line in reader:
                newrow = []
                # Database.debug(line)
                for col in line:
                    colPos = line.index(col)
                    # Database.debug("\nthis column in position %d and pre-scrub value is %s" % (colPos,col))
                    if colPos in self.phoneColList:
                        # Database.debug("this column index is in the list %s and will be scrubbed" % self.phoneColList)
                        col = Database.scrub(col)
                        if len(col) == 10 or len(col) == 0:
                            pass
                        else:
                            Database.debug("Column %s has value %s which is not a 10 digit phone number." % (self.headers[colPos], line[colPos]))
                        # Database.debug("new value is %s\n" % col)
                    newrow.append(str(col))
                # Database.debug("This should be 1 row: %s" % newrow)
                cleanfile.write(','.join(newrow) + '\n')
            cleanfile.close()
        return True

    def createTable(self):
        self.cols = []
        self.cols_set = []
        query = "create table dnc.`%s` (dncinternalid int not null auto_increment" % self.time_in
        for header in self.headers:
            if self.headers.index(header) in self.phoneColList:
                query += ", `%s` bigint" % header
            else:
                query += ", `%s` text" % header
            self.cols.append("@col"+str((self.headers.index(header)+1)))
            self.cols_set.append("`%s`=@col%s" % (header, (self.headers.index(header)+1)))
        query += ", PRIMARY KEY (dncinternalid))"
        Database.doQuery(query)
        return True

    def importTable(self):
        query = "LOAD DATA LOCAL INFILE '%s' INTO TABLE dnc.`%s` FIELDS TERMINATED BY ',' IGNORE 1 LINES (%s) set %s" \
                % (self.path_in, self.time_in, ','.join(self.cols), ','.join(self.cols_set))
        # Database.debug(query)
        Database.doQuery(query)
        return True

    def cleanup(self):
        query = "delete from dnc.`%s` where " % self.time_in
        for i in self.phoneColList:
            if self.phoneColList[0] == i:
                query += " `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[i]
            else:
                query += " or `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[i]
        # Database.debug(query)
        Database.doQuery(query)
        query = "select count(*) from `%s`" % self.time_in
        self.post_record_count = int(Database.getResult(query, True)[0])
        # Database.debug("there are %s records left in the table. %s were removed"
        #                % (self.post_record_count, self.record_count - self.post_record_count))
        return True

    def postToLog(self):
        query = """insert into dnc.logs (
        userid, 
        file_in_name, 
        file_in_record_count, 
        file_in_timestamp, 
        file_out_name, 
        file_out_record_count, 
        file_out_timestamp
        ) values (%d,'%s',%d,'%s','%s',%d,'%s')""" \
                % (session.get('userid'),
                   self.filename,
                   self.record_count,
                   self.time_in,
                   self.filename_out,
                   self.post_record_count,
                   self.time_out)
        # Database.debug(query)
        Database.doQuery(query)
        # Database.debug("posted to log!")
        return True

    def exportTable(self):
        query = "SELECT * FROM dnc.`%s`" % self.time_in
        result_tuple = Database.getResult(query)
        # Database.debug(result_tuple)
        writer = csv.writer(open(self.path_out, "wb"))
        # Database.debug("able to create this file")
        toprow = self.headers
        toprow.insert(0, 'id')
        # Database.debug(toprow)
        writer.writerow(toprow)
        # Database.debug("headers are in")
        for row in result_tuple:
            writer.writerow(row)
        # Database.debug("rows are in")
        return True

    def delete(self):
        # if self.time_in:
        query = "DROP TABLE dnc.`%s`" % self.time_in
        Database.doQuery(query)
        # delete mysql imported file from server.
        if os.path.exists(self.path_in):
            os.remove(self.path_in)
        # I want to keep the user orignal prc files for now in case we need to Database.debug anything
        # if os.path.exists("%s.prc" % self.path_in):
        #     os.remove("%s.prc" % self.path_in)
        return True
