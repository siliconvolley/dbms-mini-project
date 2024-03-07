import MySQLdb.cursors
from flask import Flask, redirect, render_template, session, request, flash, url_for, jsonify
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
 
@app.route('/company', methods = ['POST', 'GET'])
def company_login():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT CompanyID FROM COMPANY ORDER BY CompanyID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_company_id = result['CompanyID'] if result else None
        new_company_id = increment_id(latest_company_id)
        cursor.close()
        
        return render_template('company.html', latest_company_id=new_company_id)
     
    if request.method == 'POST':
        CompanyName = request.form['CompanyName']
        Location = request.form['Location']
        Contact = request.form['Contact']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT CompanyID FROM COMPANY ORDER BY CompanyID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_company_id = result['CompanyID'] if result else None
        new_company_id = increment_id(latest_company_id)

        cursor.execute("INSERT INTO COMPANY VALUES(%s,%s,%s,%s)",(new_company_id,CompanyName, Location, Contact))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

@app.route('/company_data')
def display_company_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM COMPANY")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_company_data.html', data=data)
    except Exception as e:
        print("Error fetching data:", str(e))
        return "Error fetching data. Please check the console for details."
    
@app.route('/equipments', methods = ['POST', 'GET'])
def equipments_login():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT EquipmentID FROM EQUIPMENTS ORDER BY EquipmentID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_equipment_id = result['EquipmentID'] if result else None
        new_equipment_id = increment_id(latest_equipment_id)
        cursor.close()
        
        return render_template('equipments.html', latest_equipment_id=new_equipment_id)
     
    if request.method == 'POST':
        EquipmentName = request.form['EquipmentName']
        PowerRating = request.form['PowerRating']
        ManufacturingDate = request.form['ManufacturingDate']
        CompanyID = request.form['CompanyID']        

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT CompanyID FROM COMPANY ORDER BY CompanyID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_equipment_id = result['EquipmentID'] if result else None
        new_equipment_id = increment_id(latest_equipment_id)

        cursor.execute(" INSERT INTO EQUIPMENTS VALUES(%s,%s,%s,%s,%s)",(new_equipment_id, EquipmentName, PowerRating, ManufacturingDate, CompanyID))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
    
@app.route('/equipments_data')
def display_equipments_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM EQUIPMENTS")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_equipments_data.html', data=data)
    except Exception as e:
        print("Error fetching data:", str(e))
        return "Error fetching data. Please check the console for details."
    
@app.route('/operators', methods = ['POST', 'GET'])
def operators_login():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT OperatorID FROM OPERATORS ORDER BY OperatorID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_operator_id = result['OperatorID'] if result else None
        new_opeator_id = increment_id(latest_operator_id)
        cursor.close()

        return render_template('operators.html', latest_operator_id=new_opeator_id)
     
    if request.method == 'POST':
        OperatorID = request.form['OperatorID']
        OperatorName = request.form['OperatorName']
        Occuption = request.form['Occuption']
        PhoneNumber = request.form['PhoneNumber']
        CompanyID = request.form['CompanyID']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT OperatorID FROM OPERATORS ORDER BY OperatorID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_operator_id = result['OperatorID'] if result else None
        new_opeator_id = increment_id(latest_operator_id)

        cursor.execute("INSERT INTO OPERATORS VALUES(%s,%s,%s,%s,%s)",(new_opeator_id, OperatorName, Occuption, PhoneNumber, CompanyID))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
    
@app.route('/operators_data')
def display_operators_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM OPERATORS")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_operators_data.html', data=data)
    except Exception as e:
        print("Error fetching data:", str(e))
        return "Error fetching data. Please check the console for details."

# Function to increment the retrieved IDs
def increment_id(id):
    prefix = id[:1]
    num = id[1:]

    num = int(num) + 1
    num = str(num).zfill(3)

    return prefix + num

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
