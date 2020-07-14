from flask import Flask
from flask import render_template
from flask import request

import sqlite3 as sql

app = Flask(__name__)


@app.route('/admin')
def admin_login():
    return render_template('adminlogin.html')

@app.route('/validate_admin',methods=['POST'])
def validateAdmin():
    uname=request.form.get('uname')
    password=request.form.get('password')
    if uname=="mounika" and password=="Mounika1":
        return render_template('adminwelcome.html')
    else:
        message={'message':"Invalid Details"}
        return render_template("adminlogin.html",msg=message)

@app.route('/adminwelcome')
def adminWelcome():
    return render_template('adminwelcome.html')

@app.route('/scheduleclass')
def scheduleNewClass():
    return render_template('scheduleclass.html')

@app.route('/savecourse',methods=['POST'])
def saveCourse():
    name=request.form.get("name")
    faculty=request.form.get("faculty")
    date=request.form.get("date")
    time=request.form.get("time")
    fee=request.form.get("fee")
    duration=request.form.get("duration")
    print(name,faculty,date,time,fee,duration)
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()

    curs.execute("select max(cno)from course")
    res=curs.fetchone()
    if res[0]:
        cno=res[0]+1
    else:
        cno=1001
    curs.execute("insert into course values(?,?,?,?,?,?,?)",(cno,name,faculty,date,time,fee,duration))
    conn.commit()
    conn.close()
    return render_template('scheduleclass.html',message="Saved Successfully")

@app.route('/viewscheduleclass')
def viewScheduleClass():
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("select * from course")
    res=curs.fetchall()
    return render_template('viewclass.html',data=res)

@app.route('/updateclass')
def updateClass():
    no=request.args.get('u')
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("select *from course where cno=?",(no,))
    res = curs.fetchone()
    return render_template('update_scheduleclass.html',data=res)

if __name__ == '__main__':
    app.run(debug=True)
