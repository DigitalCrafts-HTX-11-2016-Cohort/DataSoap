# coding=utf-8
import os, datetime, csv
import pymsgbox.native as pymsgbox
from database import Database
# import sys
from flask import Flask, render_template, request, redirect, session, send_file
from werkzeug.utils import secure_filename

# reload(sys)
# sys.setdefaultencoding('utf8')

ALLOWED_EXTENSIONS = {'txt', 'csv'}

#define connection

app = Flask(__name__)
app.secret_key = 'wnaptihtr'
#for local testing
app.config['UPLOAD_FOLDER'] = "static/files_in/"
app.config['DOWNLOAD_FOLDER'] = "static/files_out/"

#for live
# app.config['UPLOAD_FOLDER'] = "/var/www/FlaskApp/DNCApp/static/files_in/"
# app.config['DOWNLOAD_FOLDER'] = "/var/www/FlaskApp/DNCApp/static/files_out/"
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


def debug(line):
    # local debug target
    target = open("static/debug.log", "a")
    # live debug target
    # target = open("/var/www/FlaskApp/DNCApp/debug.log", "a")
    ip = request.remote_addr
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%f")
    target.write("\n[%s][%s] %s"%(timestamp,ip, line))
    target.close()


def allowed_file(filename):
    filename_pieces = filename.rsplit('.', 1)
    debug(filename_pieces)
    if len(filename_pieces)>2:
        return False
    return '.' in filename and \
           filename_pieces[1].lower() in ALLOWED_EXTENSIONS


# noinspection PyTypeChecker
@app.route('/searchResult', methods=['POST', 'GET'])
def searchResult():
    debug("searchResult function initiated")
    numberSearched = Database.scrub(request.args.get('number'))
    query = "select dncinternalid from dnc.`master` where master.PhoneNumber = %d" % int(numberSearched)
    query_result = Database.getResult(query,True)
    debug(query_result)
    if query_result:
        result="DO NOT CALL this number"
    else:
        result="This number is Squeaky Clean!"
    return '{"result":"%s"}' % result


class Users:
    def __init__(self,id = 0):
        self.firstname = ""
        self.lastname = ""
        self.company = ""
        self.email = ""
        self.username = ""
        self.password = ""
        self.id = id

    def save(self):
        if self.id>0:
            return self.update()
        else:
            return self.insert()

    def insert(self):
        debug(type(self.firstname))
        debug(type(self.lastname))
        debug(type(self.company))
        query = ("insert into dnc.users (firstname, lastname, company, email, username, password) values ('%s','%s','%s','%s','%s','%s')"%(Database.escape(self.firstname),Database.escape(self.lastname),Database.escape(self.company),self.email,self.username,self.password))
        lastID = Database.doQuery(query)
        return lastID

    def update(self):
        query = ("update dnc.users set firstname = '%s', lastname= '%s', company= '%s', email= '%s', password= '%s' where id=%d"%(Database.escape(self.firstname),Database.escape(self.lastname),Database.escape(self.company),self.email,self.password,self.id))
        Database.doQuery(query)
        return True


class Userfile:
    def __init__(self, filename, time_in = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%f")):
        self.filename = filename
        self.path_in = app.config['UPLOAD_FOLDER']+self.filename
        self.time_in = time_in
        self.time_out = ""
        self.filename_out = self.time_in+self.filename[8:]
        self.path_out = app.config['DOWNLOAD_FOLDER']+str(session.get('userid'))+"/"+self.filename_out


    def findPhoneCols(self):
        os.rename(self.path_in,("%s.prc" % self.path_in))
        prc_file = open("%s.prc" % self.path_in)
        # debug("changed original to .prc")
        dReader = csv.DictReader(prc_file)
        cleanfile = open(self.path_in, "w")
        self.headers = dReader.fieldnames
        self.record_count = sum(1 for row in dReader)
        # debug("headers from old file are: %s" % self.headers)
        self.phoneColList = []
        with open("%s.prc" % self.path_in) as prc_file:
            reader = csv.reader(prc_file)
            for i in range(3):
                row = reader.next()
                for col in row:
                    if len(Database.scrub(col)) == 10 and Database.is_int(col):
                        # debug("This col index should be added %d" % row.index(col))
                        if row.index(col) not in self.phoneColList:
                            self.phoneColList.append(row.index(col))
                # debug(self.phoneColList)
            if not self.phoneColList:
                session['success_message']="There were no recognized phone numbers in you file<br />If you have extensions or country codes, please remove those and try again"
                return redirect('/dashboard')

            prc_file.seek(0)
            # debug(self.record_count)
            for line in reader:
                newrow = []
                # debug(line)
                for col in line:
                    colPos = line.index(col)
                    # debug("\nthis column in position %d and pre-scrub value is %s" % (colPos,col))
                    if colPos in self.phoneColList:
                        # debug("this column index is in the list of %s and will be scrubbed" % self.phoneColList)
                        col = Database.scrub(col)
                        # debug("new value is %s\n" % col)
                    newrow.append(str(col))
                # debug("This should be 1 row: %s" % newrow)
                cleanfile.write(','.join(newrow)+ '\n')
            cleanfile.close()
        return True

    def createTable(self):
        self.cols = []
        self.cols_set = []
        query="create table dnc.`%s` (dncinternalid int not null auto_increment" % self.time_in
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
        query="LOAD DATA LOCAL INFILE '%s' INTO TABLE dnc.`%s` FIELDS TERMINATED BY ',' IGNORE 1 LINES (%s) set %s" % (self.path_in, self.time_in, ','.join(self.cols), ','.join(self.cols_set))
        # debug(query)
        Database.doQuery(query)
        return True

    def cleanup(self):
        query="delete from dnc.`%s` where " % self.time_in
        for i in self.phoneColList:
            if self.phoneColList[0] == i:
                query+=" `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[i]
            else:
                query+=" or `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[i]
        debug(query)
        Database.doQuery(query)
        query="select count(*) from `%s`" % self.time_in
        self.post_record_count = int(Database.getResult(query,True)[0])
        debug("there are %s records left in the table. %s were removed" % (self.post_record_count,self.record_count - self.post_record_count))
        return True

    def postToLog(self):
        query="insert into dnc.logs (userid,file_in_name,file_in_record_count,file_in_timestamp,file_out_name,file_out_record_count,file_out_timestamp) values (%d,'%s',%d,'%s','%s',%d,'%s')" % (session.get('userid'),self.filename,self.record_count,self.time_in,self.filename_out,self.post_record_count,self.time_out)
        debug(query)
        Database.doQuery(query)
        debug("posted to log!")
        return True

    def exportTable(self):
        query="SELECT * FROM dnc.`%s`" % self.time_in
        result_tuple = Database.getResult(query)
        debug(result_tuple)
        writer = csv.writer(open(self.path_out,"wb"))
        debug("able to create this file")
        toprow = self.headers
        toprow.insert(0,'id')
        debug(toprow)
        writer.writerow(toprow)
        debug("headers are in")
        for row in result_tuple:
            writer.writerow(row)
        debug("rows are in")
        return True

    def delete(self):
        # if self.time_in:
        query="DROP TABLE dnc.`%s`" % self.time_in
        Database.doQuery(query)
        #delete mysql imported file from server.
        if os.path.exists(self.path_in):
            os.remove(self.path_in)
        #I want to keep the user orignal prc files for now in case we need to debug anything
        # if os.path.exists("%s.prc" % self.path_in):
        #     os.remove("%s.prc" % self.path_in)
        return True

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    if 'username' in session:
        return redirect('/dashboard')
    else:
        return render_template("login.html")

@app.route('/new_user', methods = ['GET', 'POST'])
def new_user():
    return render_template("registration.html")

@app.route("/new_user_submit", methods = ['GET', 'POST'])
def new_user_submit():
    # id=request.form.get('id')
    users = Users()
    users.firstname = request.form.get('firstname')
    users.lastname = request.form.get('lastname')
    users.company = request.form.get('company')
    users.email = request.form.get('email')
    users.username = request.form.get('username')
    users.password = request.form.get('password')
    password1 = request.form.get('password1')
    if users.password == password1:
        id = users.insert()
        os.mkdir(app.config['DOWNLOAD_FOLDER'] + str(id), 0o777)
    else:
        return ("Sorry your password does not match, click back and try again!")
    return redirect("/login")


# noinspection PyTypeChecker
@app.route("/submit_login", methods = ['GET', 'POST'])
def submit_login():
    users = Users(id)
    users.username = request.form.get('username')
    users.password = request.form.get('password')
    query = "select id from dnc.users where username = '%s' and password = '%s'" % (users.username, users.password)
    debug(query)
    foo = Database.getResult(query,True)
    try:
        if len(foo) > 0:
            debug("This User exists and password true")
            session['username'] = users.username
            session['logged in'] = True
            session['userid'] = foo[0]
            debug(session.get('userid'))
            debug(session.get('username'))
            return redirect("/dashboard")
    except TypeError as exception:
        pymsgbox.alert('Login Failed. Redirecting', 'Alert!')
        debug("Failed login. Alert should have popped up.")
        # time.sleep(5)
        return redirect('/login')


@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    if 'username' in session:
        debug(session.get('username'))
        return render_template("dashboard.html")
    return redirect('/')

@app.route("/reports", methods = ['GET', 'POST'])
def report():
    if 'userid' in session:
        query = "select str_to_date(file_in_timestamp,'%%Y%%m%%d') as `Date`,avg(TIMESTAMPDIFF(SECOND, str_to_date(file_in_timestamp,'%%Y%%m%%d%%H%%S'), str_to_date(file_out_timestamp,'%%Y%%m%%d%%H%%S'))) as SecondsToProcess,avg(file_out_record_count/file_in_record_count) as CleanPercentage from dnc.logs where userid=%d group by `Date`" % session.get('userid')
        avg_ptime_clean = Database.getResult(query)
        debug(avg_ptime_clean)
        return render_template("reports.html", avg_ptime_clean = avg_ptime_clean)
    return redirect('/')

@app.route("/history", methods = ['GET', 'POST'])
def history():
    if 'userid' in session:
        query = """select 
        file_in_name,
        str_to_date(file_in_timestamp,'%%Y%%m%%d') as `Date`,
        file_in_record_count - file_out_record_count as records_removed, 
        file_out_record_count,
        file_out_name
        from dnc.logs 
        where userid = %d 
        order by `Date` desc""" % session.get('userid')
        logHistory = Database.getResult(query)
        # debug(logHistory)
        return render_template("history.html", logHistory = logHistory)
    return redirect('/')

@app.route("/profile", methods = ['GET', 'POST'])
def profile():
    session.get('username')
    if 'username' in session:
        id = request.args.get('id')
        # users = Users(id)
        username = session.get('username')
        if 'username' in session:
            query = "select * from dnc.users where username = '%s'" % username
            prof = Database.getResult(query,True)
            id = int(prof[0])
            firstname = prof[1]
            lastname = prof[2]
            company = prof[3]
            email = prof[4]
            password = prof[6]
            return render_template("profile.html", firstname=firstname, lastname=lastname, company=company, email=email, username=username, password=password, id=id)
    else:
        return redirect('/')


# noinspection PyTypeChecker
@app.route("/submit_profile_update", methods = ['GET', 'POST'])
def update_profile():
    session.get('username')
    users = Users(id)
    if 'username' in session:
        users.firstname = request.form.get('firstname')
        users.lastname = request.form.get('lastname')
        users.company = request.form.get('company')
        users.email = request.form.get('email')
        users.password = request.form.get('password')
        users.id = session.get('userid')
        users.update()
    return redirect('/dashboard')

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route("/main_page", methods = ['GET', 'POST'])
def main_page():
    if 'success_message' in session:
        del session['success_message']
    return redirect('/')


@app.route('/process', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and request.files['Select csv']:
        microseconds = datetime.datetime.utcnow().strftime("%S%f")
        f = request.files['Select csv']
        if allowed_file(f.filename):
            pass
        else:
            session['success_message'] = "<h3>Only txt and csv files are supported at this time - Please try again.</h3>"
            return redirect ("/dashboard")
        userfile = Userfile(microseconds+secure_filename(f.filename).lower())
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],userfile.filename))
        session['time_in'] = userfile.time_in
        session['filename'] = userfile.filename
        debug("***********")
        debug("About to debug time_in and then filename for uploaded file")
        debug(session.get('time_in'))
        debug(userfile.filename)
        debug("***********")
        debug("about to findPhoneCols")
        userfile.findPhoneCols()
        debug("about to createTable")
        userfile.createTable()
        debug("about to importTable")
        userfile.importTable()
        debug("File uploaded successfully with %d records" % userfile.record_count)
        userfile.cleanup()
        userfile.time_out = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%f")
        userfile.postToLog()
        debug("successfully posted to logs")
        success_message = "File uploaded successfully with %d original records<br />We scrubbed %d out and %d remain<br />Your data was %d%% dirty... Now it's DataSoap clean! <br /> <a href=\"/download\">Click to download</a> " % (userfile.record_count,(userfile.record_count-userfile.post_record_count),userfile.post_record_count,float((float(userfile.record_count-userfile.post_record_count)/userfile.record_count)*100))
        session['success_message'] = success_message
        debug("About to export clean file to files out")
        userfile.exportTable()
        debug("Successfully exported file!")
        debug("about to delete")
        userfile.delete()
        debug("delete function complete")
        return redirect ("/dashboard")
    else:
        session['success_message'] = "<h3>No File Selected - Please try again.</h3>"
        return redirect ("/dashboard")

@app.route('/download', methods = ['GET', 'POST'])
def download():
    # debug("Sending the file to user side")
    return send_file(app.config['DOWNLOAD_FOLDER']+str(session.get('userid'))+"/"+session.get('time_in')+session.get('filename')[8:],as_attachment=True, attachment_filename=session.get('filename')[8:])

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
   app.run()
