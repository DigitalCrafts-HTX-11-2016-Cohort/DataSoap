import os, sys, mysql.connector, datetime, csv
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from werkzeug.utils import secure_filename

reload(sys)
sys.setdefaultencoding('utf8')


#adding a comment to test

#define connection

app = Flask(__name__)

app.secret_key = 'wnaptihtr'
#for local testing
# app.config['UPLOAD_FOLDER'] = "static/files_in/"
# app.config['DOWNLOAD_FOLDER'] = "static/files_out/"
# #for live
# app.config['UPLOAD_FOLDER'] = "/var/www/FlaskApp/DNCApp/static/files_in/"
# app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
# home_dir = os.path.join(app.config['UPLOAD_FOLDER'],"")


class Database:
    @staticmethod
    def escape(value):
        return value.replace("'","''")

    @staticmethod
    def getConnection():
        return mysql.connector.connect(
            user='root',
            password='',
            host='127.0.0.1',
            database='users')

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

class Users:
    def __init__(self,id=0):
        self.firstname= ""
        self.lastname= ""
        self.company= ""
        self.email= ""
        self.username= ""
        self.password= ""

    def save(self):
        if self.id>0:
            return self.update()
        else:
            return self.insert()

    def insert(self):
        query = ("insert into users (firstname, lastname, company, email, username, password) values ('%s','%s','%s','%s','%s','%s')"%(Database.escape(self.firstname),Database.escape(self.lastname),Database.escape(self.company),self.email,self.username,self.password))
        Database.doQuery(query)
        return True

    def update(self):
        query = ("update users set (firstname, lastname, company, email, username, password) values ('%s','%s','%s','%s','%s','%s') where id=%d"%(Database.escape(self.firstname),Database.escape(self.lastname),Database.escape(self.company),self.email,self.username,self.password,self.id))
        Database.doQuery(query)
        return True
    #
    # def delete(self):
    #     query = ("delete from users where id=%d"% self.id
    #     Database.doQuery(query)
    #     return True

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("login.html")

@app.route('/new_user', methods = ['GET', 'POST'])
def new_user():
    return render_template("registration.html")

@app.route("/new_user_submit", methods = ['GET', 'POST'])
def new_user_submit():
    id=request.form.get('id')
    users = Users()
    users.firstname=request.form.get('firstname')
    users.lastname=request.form.get('lastname')
    users.company=request.form.get('company')
    users.email=request.form.get('email')
    users.username=request.form.get('username')
    query = "select username from dnc.users where username = request.form.get('username')"
    test = Database.getResult(query,True)
    if len(test) > 0:
        return "Sorry username has been taken, click back and try again!"
    else:
        pass
    users.password=request.form.get('password')
    password1=request.form.get('password1')
    if users.password == password1:
        users.insert()
    return redirect("/new_user_submit")

@app.route("/submit_login", methods = ['GET', 'POST'])
def submit_login():
    users = Users(id)
    users.username = request.form.get('username')
    users.password = request.form.get('password')
    query = "select * from users where username = '%s' and password = '%s'" % (users.username, users.password)
    print query
    foo = Database.getResult(query)
    if len(foo) > 0:
        print "This User exists and password true"
        session['username'] = users.username
        session['logged in'] = True
        print session.get('username')
        return render_template("dashboard.html",firstname=users.firstname,username=users.username)
    else:
        print "failed condition"
        return redirect('/')

@app.route("/logout", methods= ['GET', 'POST'])
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
