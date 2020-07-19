from flask import Flask
from flask import render_template
from flask import request
from flask import session

import sqlite3 as sql

app = Flask(__name__)

app.secret_key="mouni" #session secret key was set
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

@app.route('/update',methods=['POST'])
def update():
    no=request.form.get("no")
    name = request.form.get("name")
    faculty = request.form.get("faculty")
    date = request.form.get("date")
    time = request.form.get("time")
    fee = request.form.get("fee")
    duration = request.form.get("duration")
    print(no,name, faculty, date, time, fee, duration)
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    res=curs.execute("update course SET course_name=?,faculty_name=?,class_date=?,class_time=?,fee=?,duration=? where cno=?", (name,faculty,date,time,fee,duration,no))
    conn.commit()
    return viewScheduleClass()

@app.route('/deleteclass')
def deleteClass():
    no=request.args.get('u')
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    res = curs.execute(
        "delete from course where cno=?",(no,))
    conn.commit()
    return viewScheduleClass()

@app.route('/main')
def student():
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("select *from course")
    res = curs.fetchall()
    return render_template('main.html',data=res)

@app.route('/register')
def register():
    return render_template('student_registration.html')

@app.route('/regsave',methods=['POST','GET'])
def saveRegistration():
    name = request.form.get('name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    password = request.form.get('password')
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("select max(id)from student_registration")
    res = curs.fetchone()
    if res[0]:
        id = res[0] + 1
    else:
        id = 1
    try:
        curs.execute("insert into student_registration values(?,?,?,?,?)",(id,name,contact,email,password))
        conn.commit()
        conn.close()
        return render_template('student_login.html')
    except:
        return render_template('student_registration.html',data="Name or Contactus already registered")

@app.route('/loginstudent')
def loginstudent():
    return render_template('student_login.html')

@app.route('/studentlogin',methods=['POST'])
def student_login():
    uname=request.form.get('uname')
    pwd = request.form.get('password')
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("select *from student_registration")
    res = curs.fetchall()
    # print(res)
    for x in res:
        if uname==x[1] and pwd==x[4]:
            session['user']=uname # session created

            session['id']=x[0]
            # print(session['id'])
            # print(uname,x[1],pwd,x[4])
            return render_template('welcomestudent.html',data=session['user'])

    return render_template('student_login.html',data="Invalid Credentials")

@app.route('/enrollcourse')
def enrollcourse():
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("Select *from course")
    res=curs.fetchall()
    return render_template('enrollcourse.html',data=res)

@app.route('/enrollsave',methods=['GET'])
def enrollsave():
    cno=request.args.get('x')
    id=session['id']
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("select *from studentenrollment")
    res=curs.fetchall()
    if res:
        print(res)
        for x in res:
            if x[1]==int(cno):
                curs.execute("Select *from course")
                res = curs.fetchall()
                return render_template('enrollcourse.html',data1="Course already registered",data=res)


    curs.execute("insert into studentenrollment values(?,?)", (id, cno))
    conn.commit()

    return render_template('viewallenrolledcourses.html')

@app.route('/viewenrolledcourse',methods=['GET'])
def viewEnrolledCourse():
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("select course.cno,course.course_name,course.faculty_name,course.class_date,course.class_time,course.fee,course.duration from course"
                 " join studentenrollment on studentenrollment.courseid=course.cno")

    res = curs.fetchall()
    # print(res)
    return render_template('viewenrollcourse.html',data=res)

@app.route('/cancelenroll')
def cancelEnroll():
    cno=request.args.get('cno')
    conn = sql.connect("mounika.sqlite2")
    curs = conn.cursor()
    curs.execute("delete from studentenrollment where courseid=?",(cno,))
    conn.commit()
    curs.execute(
        "select course.cno,course.course_name,course.faculty_name,course.class_date,course.class_time,course.fee,course.duration from course"
        " join studentenrollment on studentenrollment.courseid=course.cno")

    res = curs.fetchall()
    return render_template('viewenrollcourse.html',data=res)

if __name__ == '__main__':
    app.run(debug=True)
