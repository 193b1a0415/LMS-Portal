from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import mysql.connector
import os
from datetime import date 
from datetime import datetime
app = Flask(__name__)
db = mysql.connector.connect(host="localhost",user="root",password="",database="lms" )
c=db.cursor()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/addBookDB',methods=["GET"])
def addBooksDB():
    bn=request.args['bname']
    an=request.args['aname']
    bp=request.args['bprice']
    bi=request.args['bisbn']
    sql="insert into books values('%s','%s','%s','%s')"%(bn,an,bp,bi)
    c.execute(sql)
    db.commit()
    return render_template('addBooks.html')


@app.route('/UpdateBookDB',methods=["GET"])
def UpdateBookDB():
    bn=request.args['bname']
    an=request.args['aname']
    bp=request.args['bprice']
    bi=request.args['bisbn']
    sql="update books set bname='%s' ,aname='%s' ,bprice=%s where bisbn=%s"%(bn,an,bp,bi)
    print("Update "+sql)
    c.execute(sql)
    db.commit()
    sql = "SELECT * FROM books"
    c.execute(sql)
    data = c.fetchall()
    return render_template('viewbooks.html',ddata=data)


@app.route('/IssueBooksDB',methods=["GET"])
def IssueBooksDB():
    isbn=request.args['isbn']
    userid=request.args['userid']
    sql="insert into issuebook(isbn,userid) values('%s','%s')"%(isbn,userid)
    c.execute(sql)
    db.commit()
    return render_template('adminhome.html')


@app.route('/viewBooks')
def viewBooks():
    cursor = db.cursor()
    
    sql = "SELECT * FROM books"
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('viewbooks.html',ddata=data)

@app.route('/EditBook',methods=['GET'])
def EditBook():
    isbn=request.args['isbn']
    cursor = db.cursor()
    sql = "SELECT * FROM books where bisbn="+str(isbn)
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('EditBook.html',ddata=data)


@app.route('/DeleteBook',methods=['GET'])
def DeleteBook():
    isbn=request.args['isbn']
    cursor = db.cursor()
    sql="delete from books where bisbn="+str(isbn)
    cursor.execute(sql)
    db.commit()
    sql = "SELECT * FROM books"
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('viewbooks.html',ddata=data)


@app.route('/IssueBooks')
def IssueBooks():
    cursor = db.cursor()
    
    sql = "SELECT * FROM books"
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    sql = "SELECT * FROM users"
    rows_count = cursor.execute(sql)
    userdata = cursor.fetchall()
    return render_template('IssueBooks.html',ddata=data,userdata=userdata)

@app.route('/viewIssuedBooks')
def viewIssuedBooks():
    cursor = db.cursor()
    
    sql = "SELECT bname,aname,bprice,name,email,phno FROM books b,users u,issuebook i where b.bisbn=i.isbn and u.userid=i.userid;"
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('viewIssuedBooks.html',ddata=data)


@app.route('/addBooks')
def addBooks():
    return render_template('addBooks.html')


@app.route('/signup')
def signup():
    return render_template('index.html')
   
@app.route('/userregister')
def userregister():
    return render_template('registration.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/userlogin')
def userlogin():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('inde.html')




@app.route('/userregisterdb', methods=['POST'])
def do_userregisterdb():
    uid=request.form['userid']
    name=request.form['name']
    email=request.form['email']
    phno=request.form['phno']
    area=request.form['area']
    password=request.form['password']
    
    
    cursor = db.cursor()
    cursor.execute('insert into users values("%s", "%s", "%s", "%s", "%s","%s")' % \
             (uid,name,email,phno,area,password))
    db.commit()
    
    return render_template('index.html')

    
@app.route('/login', methods=['POST'])
def do_login():
    flag=False
    cursor = db.cursor()
    username=request.form['username']
    password=request.form['password']
    sql = "SELECT * FROM users WHERE userid= '%s' and password = '%s' " % (username,password)
    print("Sql  is ",sql)
    cursor.execute(sql)
    rows_count = cursor.fetchall()
    if len(rows_count) > 0:
        session['logged_in'] = True
        session['uid'] = username
        flag=True
    else:
        flag=False
    if flag:
        return render_template('userhome.html')
    else:
        return render_template('index.html')

#admin module starts

@app.route('/adminlogin', methods=['POST'])
def do_adminlogin():
    flag=False
    ##print ("Admin Login")
    username=request.form['username']
    password=request.form['password']
    if username=='admin' and password=='admin':
        session['logged_in'] = True
        flag=True
    else:
        flag=False
    if flag:
        return render_template('adminhome.html')
    else:
        return render_template('index.html')


@app.route('/viewfeedback')
def do_viewfeedbackdb():
    ##print ("Welcome feedback view")
    cursor = db.cursor()
    
    sql = "SELECT users.userid,name,feedback,date,time FROM users,feedback where users.userid=feedback.userid"
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('viewfeedback.html',ddata=data)

@app.route('/viewadminfeedback')
def do_viewadminfeedbackdb():
    ##print ("Welcome feedback view")
    cursor = db.cursor()
    
    sql = "SELECT users.userid,name,feedback,date,time FROM users,feedback where users.userid=feedback.userid"
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('viewadminfeedback.html',ddata=data)


@app.route('/profile')
def profiledb():
    
    cursor = db.cursor()
    uid=session['uid']
    
    sql = "SELECT userid,name,password,area,email,phno FROM users where userid='%s'" % (uid)
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('profile.html',ddata=data)



@app.route('/UserIssueBook')
def UserIssueBook():
    cursor = db.cursor()
    uid=session['uid']
    sql =  "SELECT bname,aname,bprice,name,email,phno FROM books b,users u,issuebook i where b.bisbn=i.isbn and u.userid=i.userid and u.userid="+str(uid)
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('UserIssueBook.html',ddata=data)


@app.route('/viewusers')
def viewusersdb():
    
    cursor = db.cursor()
    
    sql = "SELECT userid,name,email,phno,area FROM users"
    rows_count = cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('viewusers.html',ddata=data)


@app.route('/userfeedbackdb', methods=['POST'])
def do_userfeedbackdb():
    #userid=request.form['userid']
    userid=uid=session['uid']
    feedback=request.form['feedback']
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cursor = db.cursor()
    cursor.execute('insert into feedback(userid,feedback,date,time) values("%s","%s","%s","%s")' % \
             (userid,feedback,today,current_time))
    db.commit()
    return render_template('userhome.html')



#admin module Ends
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
