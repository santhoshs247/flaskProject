import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def HOME():
    return "<h2>Go to <a href='/SHOW'>Show Users</a></h2>"

@app.route('/SHOW')
def SHOW():

    A = sqlite3.connect("database.db")   
    B = A.cursor()

    B.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            EMAIL TEXT
        )
    """)

    B.execute("SELECT COUNT(*) FROM USERS")
    C = B.fetchone()[0]

    if C == 0:
        B.execute("INSERT INTO USERS (NAME,EMAIL) VALUES ('SANDY','sandy@gmail.com')")
        B.execute("INSERT INTO USERS (NAME,EMAIL) VALUES ('JOHN','john@gmail.com')")
        A.commit()

    B.execute("SELECT * FROM USERS")
    D = B.fetchall()

    A.close()

    return render_template("show.html", DATA=D)

if __name__ == '__main__':
    app.run(debug=True)
