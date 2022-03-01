import sqlite3
from hashlib import sha256
import random
DBFILE="teaching.db"

def init_or_connect_DB():
    conn = sqlite3.connect(DBFILE)
    cursor=conn.cursor()
    sqlScript=["""
        CREATE TABLE users
        (
        userID INTEGER PRIMARY KEY,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        sex TEXT,
        department TEXT NOT NULL,
        type INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE courses
        (
        courseID INTEGER PRIMARY KEY,
        courseName TEXT,
        description TEXT,
        startDate Date,
        endDate Date
        );
        """,
        """
        CREATE TABLE grades
        (
        courseID INTEGER,
        userID INTEGER,
        grade INTEGER DEFAULT -1 CHECK(grade<=100),
        PRIMARY KEY(courseID,userID),
        FOREIGN KEY(courseID) REFERENCES courses(courseID),
        FOREIGN KEY(userID) REFERENCES users(userID)
        )
        """]
    for sql in sqlScript:
        #print(sql)
        try:
            cursor.executescript(sql)
            conn.commit()
        except Exception as e:
            #print(e)
            pass

    return conn

conn=init_or_connect_DB()

def register(userID,password,name,age,sex,department,userType):
    password=sha256(password.encode()).hexdigest()
    sql=F"INSERT INTO users VALUES({userID},'{password}','{name}',{age},'{sex}','{department}',{userType})"
    print(sql)
    try:
        conn.execute(sql)
        conn.commit()
        return "注册成功"
    except Exception as e:
        print(e)
        if type(e)==sqlite3.IntegrityError:
            return "此账号已注册"
        else:
            return "其他错误"

def login(userID,password):
    sql=F"SELECT * FROM users where userID={userID}"
    cursor=conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    if len(result)==0:
        return "该账号未注册，请先注册账号"
    else:
        if result[0][1]==sha256(password.encode()).hexdigest():
            return result[0]
        else:
            return "密码错误"
    conn.commit()

def update_user(userID,name,age,sex,dep):
    sql=F"UPDATE users SET name='{name}',age={age},sex='{sex}',department='{dep}' where userID={userID}"
    try:
        conn.execute(sql)
        conn.commit()
        return "更改成功"
    except Exception as e:
        print(e)
        return e

def change_password(userID,old_pw,new_pw):
    user=login(userID,old_pw)
    if type(user)==tuple:
        sql=F"UPDATE users SET password='{sha256(new_pw.encode()).hexdigest()}'where userID={userID}"
        conn.execute(sql)
        conn.commit()
        return "更改成功"

    else:
        return "原密码错误"

def choose_course(courseID,userID,grade=-1):
    sql=F"INSERT INTO grades VALUES({courseID},{userID},{grade})"
    try:
        conn.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False

def create_course(courseID,courseName,description,startDate,endDate,userID=None):
    sql=F"INSERT INTO courses VALUES({courseID},'{courseName}','{description}','{startDate}','{endDate}')"
    #print(sql)
    try:
        conn.execute(sql)
        if userID:
            choose_course(courseID,userID,-1)
            return True
        else:
            conn.commit()
    except Exception as e:
        print(e)
        return e
    #choose_course(currentUserID,courseID,"teacher")

def get_courses():
    sql="SELECT * FROM courses"
    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        result=cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return None

def get_grades(userID=None,courseID=None):
    sql=F"SELECT courses.courseID,courses.courseName,courses.startDate,courses.endDate,grades.grade FROM courses,grades where courses.courseID=grades.courseID"
    if userID:
        sql=sql+F" AND grades.userID={userID}"
    if courseID:
        sql=sql+F" AND grades.courseID={courseID}"

    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        result=cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return None

def get_students_grades(courseID):
    sql=F"""SELECT courses.courseID,courses.courseName,users.userID,users.name,grades.grade
FROM  users,courses,grades
WHERE users.userID=grades.userID AND courses.courseID=grades.courseID AND grades.courseID={courseID}"""
    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        grades=cursor.fetchall()
        teacherID_list=[row[0] for row in get_teacher(courseID)]
        grades=[list(grade) for grade in grades if grade[2] not in teacherID_list]
        return grades
    except Exception as e:
        print(e)
        return False

def update_score(userID,courseID,grade):
    grade=int(grade)
    if grade<=100:
        sql=F"UPDATE grades SET grade={grade} where userID={userID} AND courseID={courseID}"
        try:
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

def get_teacher(courseID):
    sql=F"SELECT users.userID,users.name FROM users,grades where grades.userID=users.userID AND grades.courseID={courseID} AND users.type=1"
    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        result=cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return False



def drop_course(courseID,userID):
    if courseID==-1:
        print("Error")
        return False
    sql=F"DELETE FROM grades WHERE courseID={courseID} AND userID={userID}"
    try:
        conn.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False

def course_is_chose(courseID,userID):
    courses_chose=get_grades(userID)
    for course in courses_chose:
        if course[0]==courseID:
            return True
    return False
