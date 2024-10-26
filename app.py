from flask import Flask, render_template
import psycopg2
from config import config

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(config.DATABASE_URL)
    return conn


def check_grade(score):
    if score >= 80 and score <= 100:
        return "A"
    elif score >= 70 and score < 80:
        return "B"
    elif score >= 60 and score < 70:
        return "C"
    elif score >= 50 and score < 60:
        return "D"
    elif score >= 0 and score < 50:
        return "F"
    else:
        return "คะแนนไม่ถูกต้อง"


@app.route("/")
def hello_world():
    return "<p>toto</p>"

@app.route("/home")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from students')
    students = cursor.fetchall()
    conn.close()

    for index, item in enumerate(students):
        grade = check_grade(item[3])
        students[index] = item + (grade,)

    return render_template('home.html', students=students)