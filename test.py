from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rish@bh@mysql04'
app.config['MYSQL_DB'] = 'dbms_mp_1'
 
mysql = MySQL(app)

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
 
app.run(host='localhost', port=5000)