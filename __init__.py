import os, sys, mysql.connector, datetime, csv
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from werkzeug.utils import secure_filename

reload(sys)
sys.setdefaultencoding('utf8')

ALLOWED_EXTENSIONS = set(['txt', 'xls', 'csv'])

#adding a comment to test

#define connection

app = Flask(__name__)

app.secret_key = 'wnaptihtr'
#for local testing
# app.config['UPLOAD_FOLDER'] = "static/files_in/"
app.config['DOWNLOAD_FOLDER'] = "static/files_out/"
#for live
app.config['UPLOAD_FOLDER'] = "/var/www/FlaskApp/DNCApp/static/files_in/"
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
home_dir = os.path.join(app.config['UPLOAD_FOLDER'],"")

def debug(line):
    import time
    target = open("/var/www/FlaskApp/DNCApp/debug.log", "a")
    ip=request.remote_addr
    timestamp =  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    target.write("\n[%s][%s] %s"%(timestamp,ip, line))
    target.close()

class Database:
    @staticmethod
    def escape(value):
        return value.replace("'","''")

    @staticmethod
    def getConnection():
        return mysql.connector.connect(
            user='karissa',
            password='wnaptihtr',
            host='35.166.251.127',
            database='dnc')

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

    @staticmethod
    def scrub(data):
        return filter(type(data).isdigit, data)
        # data=data.replace('(','')
        # data=data.replace(')','')
        # data=data.replace('-','')
        # data=data.replace(' ','')
        # return data

    @staticmethod
    def is_int(data):
        try:
            int(Database.scrub(data))
            return True
        except ValueError:
            return False
# class User:
#     __init__(self,id=0)
#     if(not type(id)==int):
#         id=int(id)

class Userfile:
    def __init__(self, filename, time_in=datetime.datetime.now().strftime("%B-%d-%Y-%I:%M%p")):
        self.filename = filename
        self.path_in = app.config['UPLOAD_FOLDER']+self.filename
        self.time_in =time_in
        # print self.path_in
        self.path_out=app.config['DOWNLOAD_FOLDER']+self.filename


    def findPhoneCols(self):
        os.rename(self.path_in,("%s.prc" % self.path_in))
        prc_file = open("%s.prc" % self.path_in)
        debug("changed original to .prc")
        dReader = csv.DictReader(prc_file)
        cleanfile = open(self.path_in, "w")
        self.headers = dReader.fieldnames
        self.record_count = sum(1 for row in dReader)
        debug("headers from old file are: %s" % self.headers)
        self.phoneColList = []
        with open("%s.prc" % self.path_in) as prc_file:
            reader = csv.reader(prc_file)
            for i in range(3):
                row = reader.next()
                for col in row:
                    if len(Database.scrub(col)) == 10 and Database.is_int(col):
                        debug("This col index should be added %d" % row.index(col))
                        if row.index(col) not in self.phoneColList:
                            self.phoneColList.append(row.index(col))
                # debug(self.phoneColList)
            prc_file.seek(0)
            debug(self.record_count)
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
                    # if colPos == len(self.headers)-1:
                    #     newrow.append('\n')
                debug("This should be 1 row: %s" % newrow)
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
        # print self.cols
        # print self.cols_set
        Database.doQuery(query)
        return True

    def importTable(self):
        query="LOAD DATA LOCAL INFILE '%s' INTO TABLE dnc.`%s` FIELDS TERMINATED BY ',' IGNORE 1 LINES (%s) set %s" % (self.path_in, self.time_in, ','.join(self.cols), ','.join(self.cols_set))
        # debug(query)
        Database.doQuery(query)
        return True

    def cleanup(self):
        query="delete from dnc.`%s` where " % (self.time_in)
        for i in self.phoneColList:
            if self.phoneColList[0] == i:
                query+=" `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[i]
            else:
                query+=" or `%s` in (select PhoneNumber from dnc.`master`)" % self.headers[i]
        debug(query)
        # Database.doQuery(query)
        # return True

    # def exportTable(self):
    def delete(self):
        # if self.time_in:
        query="DROP TABLE dnc.`%s`" % self.time_in
        Database.doQuery(query)
        return True

@app.route('/', methods = ['GET', 'POST'])
def home():
    debug("loading main page")
    return render_template("dashboard.html", title="DNC Dashboard")

@app.route('/process', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['Select csv']
      userfile=Userfile(secure_filename(f.filename))
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],userfile.filename))
      session['time_in']=userfile.time_in
      session['filename']=userfile.filename
    #   debug(type(session.get('time_in')))
    #   debug(userfile.filename)
      userfile.findPhoneCols()
      userfile.createTable()
      userfile.importTable()
      debug("File uploaded successfully with %d records" % userfile.record_count)
      userfile.cleanup()
      return "File uploaded successfully with %d records" % userfile.record_count

@app.route('/deleteme', methods = ['GET', 'POST'])
def deleteme():
    file_done=Userfile(session.get('filename'),session.get('time_in'))
    file_done.delete()
    # del session['time_in']
    # del session['filename']
    return redirect('/')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


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
   app.run(debug=True)
