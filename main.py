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
def home():
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True)
