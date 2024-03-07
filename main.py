import MySQLdb.cursors
from flask import Flask, redirect, render_template, session, request, flash, url_for
from flask_mysqldb import MySQL
from datetime import datetime
from config import password
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "--------"
app.config['MYSQL_DB'] = "dbms_mp_1"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# ============================================= User Interface ========================================================

@app.route('/')
def form():
    return render_template('index.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        CompanyID = request.form['CompanyID']
        CompanyName = request.form['CompanyName']
        Location = request.form['Location']
        Contact = request.form['Contact']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO COMPANY VALUES(%s,%s,%s,%s)''',(CompanyID,CompanyName, Location, Contact))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

@app.route('/display_data')   
def display_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM COMPANY")
    data = cursor.fetchall()
    cursor.close()
    return render_template('display_data.html', data=data)
 
app.run(host='localhost', port=5000)
