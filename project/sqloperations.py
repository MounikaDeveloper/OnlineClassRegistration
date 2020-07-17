import sqlite3 as sql
conn=sql.connect("mounika.sqlite2")
curs=conn.cursor()
def createCourseTable():
    curs.execute("create table course(cno number primary key,course_name text,faculty_name text,class_date date,class_time text,fee real,duration number)")
    print("Table is created")


def createStudentLoginTable():
    curs.execute(
        "create table student_registration(name text unique,contactus number unique,email text,password text)")
    print("student table is created")
createStudentLoginTable()