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
        self.path_in = settings.upload + self.filename
        self.time_in = time_in
        self.time_out = ""
        self.filename_out = self.time_in + self.filename[8:]
        self.path_out = settings.download + str(session.get('userid')) + "/" + self.filename_out
        self.phoneColDict = {}
        self.notPhoneDict = {}
        self.finalPhoneColList = []
        self.keep_processing = True

    def findPhoneCols(self):
        os.rename(self.path_in, ("%s.prc" % self.path_in))
        prc_file = open("%s.prc" % self.path_in)
        dReader = csv.DictReader(prc_file)
        cleanfile = open(self.path_in, "w")
        self.headers = dReader.fieldnames
        Database.debug(self.headers)
        for header in self.headers:
            if len(header) >= 10:
                try:
                    Database.is_phone(header)
                except:
                    pass
                else:
                    if Database.is_phone(header):
                        session['success_message'] = """Your file is missing a header row.<br />
                                    Please insert a header row and try again"""
                        self.keep_processing = False
                        return redirect('/dashboard')
        Database.debug(self.headers)
        self.record_count = sum(1 for row in dReader)
        # Database.debug("Record count for uploaded userfile is:")
        # Database.debug(self.record_count)
        if self.record_count < 10:
            Database.debug("Less than 10 rows")
            session['success_message'] = """There were not enough records in you file or you have empty rows<br />
            Please use the quick search function to scrub just a few records, or remove empty rows and try again"""
            self.keep_processing = False
            return redirect('/dashboard')
        # Database.debug("headers from old file are: %s" % self.headers)
        with open("%s.prc" % self.path_in) as prc_file:
            reader = csv.reader(prc_file)
            for i in range(self.record_count - 1):
                row = reader.next()
                for col in row:
                    if len(Database.scrub(col)) == 10 and Database.is_phone(col):
                        # Database.debug("This col index should be added %d" % row.index(col))
                        if row.index(col) not in self.phoneColDict:
                            self.phoneColDict[row.index(col)] = 1
                        else:
                            self.phoneColDict[row.index(col)] += 1
                    elif len(Database.scrub(col)) == 10:
                        if row.index(col) not in self.notPhoneDict:
                            Database.debug("Failing data is %s" % col)
                            self.notPhoneDict[row.index(col)] = 1
                        else:
                            self.notPhoneDict[row.index(col)] += 1
            Database.debug("The POTENTIAL phone column list is %s" % self.phoneColDict)
            Database.debug("The 10 Int NON-PHONE column list is %s" % self.notPhoneDict)
            self.finalPhoneColList = [x for x in self.phoneColDict if \
                                      (self.notPhoneDict.get(x, 1) / float(self.phoneColDict.get(x))) < .101]
            for x in self.phoneColDict:
                Database.debug("Col %s %d / %d = %f. Is that less than .101? %s" % \
                               (x, self.notPhoneDict.get(x, 1), self.phoneColDict.get(x),
                                (self.notPhoneDict.get(x, 1) / float(self.phoneColDict.get(x))),
                                ((self.notPhoneDict.get(x, 1) / float(self.phoneColDict.get(x))) < .101)))
            Database.debug("The FINAL phone column list is %s" % self.finalPhoneColList)
            if not self.finalPhoneColList:
                Database.debug("Phone numbers not detected")
                session['success_message'] = """There were no recognized phone number columns in you file<br />
                If you have extensions or country codes, please remove those and try again"""
                self.keep_processing = False
                Database.debug("redirecting to dashboard")
                return redirect('/dashboard')
            prc_file.seek(0)
            Database.debug("Records in file are %d" % self.record_count)
            phone_errors = []
            phone_errors_count = 0
            for line in reader:
                newrow = []
                # Database.debug(line)
                for col in line:
                    colPos = line.index(col)
                    # Database.debug("\nthis column in position %d and pre-scrub value is %s" % (colPos,col))
                    if colPos in self.finalPhoneColList:
                        # Database.debug("this column index is in the list %s and will be scrubbed" % self.phoneColList)
                        col = Database.scrub(col)
                        if (len(col) == 10 and Database.is_phone(col)) or len(col) == 0:
                            pass
                        else:
                            phone_errors.append("Column <strong>%s</strong> has value %s"
                                                % (self.headers[colPos], line[colPos]))
                            phone_errors_count += 1
                            # *** Instead of adding these in a message, we need to keep them as a malformed list and DELETE the line from the reader then proceed.
                            # Database.debug("new value is %s\n" % col)
                    newrow.append(str(col))
                # Database.debug("This should be 1 row: %s" % newrow)
                cleanfile.write(','.join(newrow) + '\n')
            if len(phone_errors):
                limit = min(9, len(phone_errors) - 1)
                message = """There were %d items in you file which are not valid phone numbers<br />
                Please correct and try again. Examples below:<br />""" % phone_errors_count
                for error in range(0, limit):
                    Database.debug(phone_errors[error])
                    message += phone_errors[error] + "<br />"
                session['success_message'] = message
                self.keep_processing = True
                # return redirect('/dashboard')
            # Database.debug("About to close cleanfile")
            # ***NOTE_TO_MAINTAINER*** if your file gets to here and you get an Internal Server Error, stop testing on
            # credentials you made on local and use production creds (which have folders created for them correctly)
            cleanfile.close()
        return True

    def createTable(self):
        self.cols = []
        self.cols_set = []
        query = "create table dnc.`%s` (dncinternalid int not null auto_increment" % self.time_in
        for header in self.headers:
            if self.headers.index(header) in self.finalPhoneColList:
                query += ", `%s` bigint" % header.strip()
            else:
                query += ", `%s` text" % header.strip()
            self.cols.append("@col" + str((self.headers.index(header) + 1)))
            self.cols_set.append("`%s`=@col%s" % (header.strip(), (self.headers.index(header) + 1)))
        query += ", deleteFlag bit null, PRIMARY KEY (dncinternalid))"
        Database.doQuery(query)
        return True

    def importTable(self):
        query = "LOAD DATA LOCAL INFILE '%s' INTO TABLE dnc.`%s` FIELDS TERMINATED BY ',' IGNORE 1 LINES (%s) set %s" \
                % (self.path_in, self.time_in, ','.join(self.cols), ','.join(self.cols_set))
        # Database.debug(query)
        Database.doQuery(query)
        return True

    def cleanup(self):

        query = "update dnc.`%s` set deleteFlag = 1 where " % self.time_in
        Database.debug("self.finalPhoneColList is %r" % self.finalPhoneColList)
        for key in self.finalPhoneColList:
            Database.debug("key is %r and list of keys is %r" %
                           (key, self.finalPhoneColList))
            if key == self.finalPhoneColList[0]:
                query += " `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[key].strip()
            else:
                query += " or `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[key].strip()
            if session['voipOk']:
                query += " or MID(`%s`,1,3) not in (select AreaCode from dnc.`PurchasedCodes`) \
                            or (" \
                         "MID(`%s`,1,7) in (SELECT prefix FROM dnc.carrierPrefixes WHERE do_not_call = 1 AND lineType != 'V') " \
                         "AND `%s` NOT IN (SELECT PhoneNumber FROM wireless_convert WHERE source = 'WTL')" \
                         ")" % (self.headers[key].strip(), self.headers[key].strip(), self.headers[key].strip())
            else:
                query += " or MID(`%s`,1,3) not in (select AreaCode from dnc.`PurchasedCodes`) \
                or (" \
                         "MID(`%s`,1,7) in (SELECT prefix FROM dnc.carrierPrefixes WHERE do_not_call = 1) " \
                         "AND `%s` NOT IN (SELECT PhoneNumber FROM wireless_convert WHERE source = 'WTL')" \
                    ")" % (self.headers[key].strip(), self.headers[key].strip(), self.headers[key].strip())
        Database.debug("Cleanup query is:")
        Database.debug(query)
        Database.doQuery(query)
        query = "select count(*) from `%s` where deleteFlag IS NULL" % self.time_in
        self.post_record_count = int(Database.getResult(query, True)[0])
        Database.debug("there are %s records left in the table. %s were removed"
                       % (self.post_record_count, self.record_count - self.post_record_count))
        return True

    def postToLog(self):
        if not settings.local:
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
        query = "SELECT * FROM dnc.`%s` where deleteFlag IS NULL" % self.time_in
        result_tuple = Database.getResult(query)
        Database.debug("Data received. About to open %s" % self.path_out)
        writer = csv.writer(open(self.path_out, "wb"))
        Database.debug("able to create this file")
        toprow = self.headers
        toprow.insert(0, 'id')
        Database.debug(toprow)
        writer.writerow(toprow)
        Database.debug("headers are in")
        for row in result_tuple:
            try:
                writer.writerow(row)
            except:
                Database.debug(row)
        Database.debug("rows are in")
        return True

    def delete(self):
        colToCheck = self.headers[self.finalPhoneColList[0] + 1]
        query = '''
        SELECT leads.*
        ,CASE
        WHEN litigator = 1 THEN 'litigator'
        WHEN dnc = 1 THEN 'DNC'
        WHEN vista_dnc = 1 THEN 'vista_dnc'
        WHEN (wireless = 1 or carrierPrefixes.do_not_call = 1) 
          and (wireless_convert.source = 'LTW' or wireless_convert.source is null) THEN 'wireless'
        ELSE 'other' END as scrubReason
        FROM dnc.`%s` leads
        left join master on leads.%s = master.PhoneNumber
        left join wireless_convert on wireless_convert.PhoneNumber = leads.%s
        left join carrierPrefixes on mid(leads.%s,1,7) = carrierPrefixes.prefix
        where deleteFlag = 1 
        ''' % (self.time_in, "`" + colToCheck + "`", "`" + colToCheck + "`", "`" + colToCheck + "`")
        Database.debug(query)
        result_tuple = Database.getResult(query)
        # Database.debug("Data received. About to open %s" % self.path_out + ".RMVD")
        writer = csv.writer(open(self.path_out + ".RMVD", "wb"))
        Database.debug("able to create the removed file")
        toprow = self.headers
        toprow.append('deleteFlag')
        toprow.append('scrubReason')
        # toprow.insert(0, 'id')  # this is already done
        # Database.debug(toprow)
        writer.writerow(toprow)
        # Database.debug("headers are in")
        for row in result_tuple:
            try:
                writer.writerow(row)
            except:
                Database.debug(row)
        Database.debug("removed file completed")
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
