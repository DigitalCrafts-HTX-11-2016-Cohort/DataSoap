# coding=utf-8
import settings as settings
from database import Database
from userfile import Userfile
from users import Users
import datetime
import os
import pymsgbox.native as pymsgbox
# import sys
from flask import Flask, render_template, request, redirect, session, send_file
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename

# reload(sys)
# sys.setdefaultencoding('utf8')

ALLOWED_EXTENSIONS = {'txt', 'csv'}

# define connection

app = Flask(__name__)
app.secret_key = 'wnaptihtr'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


def allowed_file(filename):
    filename_pieces = filename.rsplit('.', 1)
    # Database.debug(filename_pieces)
    if len(filename_pieces) > 2:
        return False
    return '.' in filename and \
           filename_pieces[1].lower() in ALLOWED_EXTENSIONS


# noinspection PyTypeChecker
@app.route('/searchResult', methods=['POST', 'GET'])
def searchResult():
    # Database.debug("searchResult function initiated")
    numberSearched = Database.scrub(request.args.get('number'))
    query = "select dncinternalid from dnc.`master` where master.PhoneNumber = %d" % int(numberSearched)
    query_result = Database.getResult(query, True)
    # Database.debug(query_result)
    if query_result:
        result = "DO NOT CALL this number"
    else:
        result = "This number is Squeaky Clean!"
    return '{"result":"%s"}' % result


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'username' in session:
        session.pop('success_message', None)
        session.pop('time_in', None)
        session.pop('filename', None)
        return redirect('/dashboard')
    else:
        return render_template("login.html")


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    return render_template("registration.html")


@app.route("/new_user_submit", methods=['GET', 'POST'])
def new_user_submit():
    # id=request.form.get('id')
    user = Users()
    user.firstname = request.form.get('firstname')
    user.lastname = request.form.get('lastname')
    user.company = request.form.get('company')
    user.email = request.form.get('email')
    user.username = request.form.get('username')
    # can't instantiate users.password as a string then change it to unicode in below block
    password0 = str(request.form.get('password'))
    password1 = str(request.form.get('password1'))
    if password0 == password1:
        hashedpw = pbkdf2_sha256.hash(password0)
        # Database.debug("this is the type and value of hashedpw before assignment")
        # Database.debug(hashedpw)
        # Database.debug(type(hashedpw))
        user.password = hashedpw
        # Database.debug("after assignment to user.password")
        # Database.debug(type(user.password))
        userid = user.insert()
        # TO DO - need to add a if username exists clause. Causes crash as of now
        os.mkdir(settings.download + str(userid), 0o777)
    else:
        return "Sorry your password does not match, click back and try again!"
    return redirect("/login")


# noinspection PyTypeChecker
@app.route("/submit_login", methods=['GET', 'POST'])
def submit_login():
    user = Users(id)
    user.username = request.form.get('username')
    user.password = request.form.get('password')
    query = "select id, password from dnc.users where username = '%s'" % user.username
    # Database.debug(query)
    foo = Database.getResult(query, True)
    try:
        if len(foo) > 0:
            # Database.debug("User exists")
            pass_to_hash = str(request.form.get('password'))
            if pbkdf2_sha256.identify(str(foo[1])):
                passCheckMethod = pbkdf2_sha256.verify(pass_to_hash, str(foo[1]))
            else:
                passCheckMethod = (pass_to_hash == foo[1])
            if passCheckMethod:
                # Database.debug("passwords matched")
                user.password = pbkdf2_sha256.hash(pass_to_hash)
                # Database.debug("in login. type check for password")
                # Database.debug(type(user.password))
                session['username'] = user.username
                session['userid'] = foo[0]
                # Database.debug(session.get('userid'))
                # Database.debug(session.get('username'))
                return redirect("/dashboard")
            else:
                # Database.debug("passwords don't match")
                pymsgbox.alert('Wrong Username or Password', 'Alert!')
                return redirect('/login')
        else:
            # Database.debug("username doesn't exist")
            pymsgbox.alert('Wrong Username or Password', 'Alert!')
            return redirect('/login')
    except TypeError as exception:
        Database.debug(exception)
        pymsgbox.alert('Login Failed. Redirecting', 'Alert!')
        Database.debug("Failed login. Alert should have popped up.")
        # time.sleep(5)
        return redirect('/login')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html")
    return redirect('/')


@app.route("/reports", methods=['GET', 'POST'])
def report():
    if 'userid' in session:
        query = """select 
        str_to_date(file_in_timestamp,'%%Y%%m%%d') as `Date`,
        mid(file_in_name,9) as Filename,
        file_out_record_count/file_in_record_count as CleanPercentage 
        from dnc.logs 
        where userid=%d and datediff(CURRENT_DATE(),file_in_timestamp) < 10
        ORDER BY `Date`desc
        limit 10""" % session.get('userid')
        avg_ptime_clean = Database.getResult(query)
        # Database.debug(avg_ptime_clean)
        return render_template("reports.html", avg_ptime_clean=avg_ptime_clean)
    return redirect('/')


@app.route("/history", methods=['GET', 'POST'])
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
        # Database.debug(logHistory)
        return render_template("history.html", logHistory=logHistory)
    return redirect('/')


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    session.get('username')
    if 'username' in session:
        username = session.get('username')
        if 'username' in session:
            query = "select * from dnc.users where username = '%s'" % username
            prof = Database.getResult(query, True)
            userid = int(prof[0])
            firstname = prof[1]
            lastname = prof[2]
            company = prof[3]
            email = prof[4]
            password = prof[6]
            return render_template("profile.html", firstname=firstname, lastname=lastname, company=company, email=email,
                                   username=username, password=password, id=userid)
    else:
        return redirect('/')


# noinspection PyTypeChecker
@app.route("/submit_profile_update", methods=['GET', 'POST'])
def update_profile():
    session.get('username')
    user = Users(id)
    if 'username' in session:
        user.firstname = request.form.get('firstname')
        user.lastname = request.form.get('lastname')
        user.company = request.form.get('company')
        user.email = request.form.get('email')
        user.password = pbkdf2_sha256.hash(str(request.form.get('password')))
        user.id = session.get('userid')
        user.update()
    return redirect('/dashboard')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route("/main_page", methods=['GET', 'POST'])
def main_page():
    if 'success_message' in session:
        session.pop('success_message', None)
    return redirect('/')


@app.route('/process', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and request.files['Select csv']:
        f = request.files['Select csv']
        if allowed_file(f.filename):
            microseconds = datetime.datetime.utcnow().strftime("%S%f")
            time_in = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%f")
            print("microseconds generated for uploaded file w good filename:")
            print(microseconds)
            pass
        else:
            session['success_message'] = "<h3>Only txt and csv files are currently supported - Please try again.</h3>"
            return redirect("/dashboard")
        leads = Userfile(microseconds + secure_filename(f.filename).lower(), time_in)
        f.save(os.path.join(settings.upload, leads.filename))
        session['time_in'] = time_in
        session['filename'] = leads.filename
        # Database.debug("***********")
        # Database.debug("About to Database.debug time_in and then filename for uploaded file")
        # Database.debug(time_in)
        # Database.debug(leads.filename)
        # Database.debug("***********")
        # Database.debug("about to findPhoneCols")
        leads.findPhoneCols()
        # Database.debug("about to createTable")
        leads.createTable()
        # Database.debug("about to importTable")
        leads.importTable()
        # Database.debug("File uploaded successfully with %d records" % leads.record_count)
        leads.cleanup()
        # leads.time_out = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%f")
        leads.postToLog()
        # Database.debug("successfully posted to logs")
        success_message = """File uploaded successfully with %d original records<br />
        We scrubbed %d out and %d remain<br />Your data was %d%% dirty... Now it's DataSoap clean! <br /> 
        <a href=\"/download\">Click to download</a> """ \
                          % (leads.record_count,
                             (leads.record_count-leads.post_record_count),
                             leads.post_record_count,
                             float((float(leads.record_count-leads.post_record_count)/leads.record_count)*100))
        session['success_message'] = success_message
        # Database.debug("About to export clean file to files out")
        leads.exportTable()
        # Database.debug("Successfully exported file!")
        # Database.debug("about to delete")
        leads.delete()
        # Database.debug("delete function complete")
        return redirect("/dashboard")
    else:
        session['success_message'] = "<h3>No File Selected - Please try again.</h3>"
        return redirect("/dashboard")


@app.route('/download', methods=['GET', 'POST'])
def download():
    # Database.debug("Sending the file to user side")
    return send_file(settings.download+str(session.get('userid'))+"/"+session.get('time_in')
                     + session.get('filename')[8:], as_attachment=True, attachment_filename=session.get('filename')[8:])


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    if settings.local:
        response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run()
