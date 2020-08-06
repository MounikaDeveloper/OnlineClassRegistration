import sqlite3 as sql
conn=sql.connect("mounika.sqlite2")
curs=conn.cursor()
def createCourseTable():
    curs.execute("create table course(cno number primary key,course_name text,faculty_name text,class_date date,class_time text,fee real,duration number)")
    print("Table is created")


def createStudentLoginTable():
    curs.execute(
        "create table student_registration(id number primary key,name text unique,contactus number unique,email text,password text)")
    print("student table is created")


def studentEnrollment():
    curs.execute("create table studentenrollment(studentid number,"
                 "courseid number,"
                 "foreign key (studentid) references student_registration(id),"
                 "foreign key(courseid) references course(cno))")
    print("student enrollment table is created")
studentEnrollment()
# curs.execute("drop table studentenrollment")