from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from datetime import datetime
from config import password

app = Flask(__name__)
app.config['SECRET_KEY'] = "--------"
app.config['MYSQL_DB'] = "dbms_mp_1"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# ============================================= User Interface ========================================================

# Login Page rendering
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM AUTH WHERE UserName = %s AND Password = %s', (username, password))
        credentials = cursor.fetchone()
        cursor.close()
        if credentials == None:
            return '<h1>Wrong Credentials</h1>'

        return render_template('home.html')

# Signup Page rendering
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM AUTH WHERE UserName = %s AND Password = %s', (username, password))
        existing_user = cursor.fetchone()
        

        if existing_user:
            return '<h1>Username and password combination already exists</h1>'

        cursor.execute('INSERT INTO AUTH (UserName, Password) VALUES (%s,%s)', (username, password))
        mysql.connection.commit()
        cursor.close()
        return redirect('/')

# Home Page Rendering
@app.route('/home')
def home_page():
    return render_template('home.html')

# Home Page Searching
@app.route('/search_equipment', methods=['GET'])
def search_equipment():
    equipment_name = request.args.get('equipment_name')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT EQUIPMENTS.*, CompanyName FROM EQUIPMENTS, COMPANY WHERE EquipmentName = %s AND EQUIPMENTS.CompanyID=COMPANY.CompanyID', (equipment_name,))
    equipment = cursor.fetchone()
    cursor.close()
    if equipment == None:
        return render_template('search_not_found.html')
    
    return render_template('search_results.html', equipment=equipment)

# Add New page rendering
@app.route('/add_new')
def add_new():
    return render_template('forms/add_new.html')

# All Equipments Overview page rendering
@app.route('/equipment_overview')
def equipment_overview():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT EquipmentID, EquipmentName FROM EQUIPMENTS')
        equipments = cursor.fetchall()
        cursor.close()

        return render_template('equipments/equipment_overview.html', equipments=equipments)

# Display Logs
@app.route('/logs')
def display_logs():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT A.*, E.EquipmentName, O.OperatorName FROM ALERTS A, EQUIPMENTS E, OPERATORS O WHERE A.EquipmentID=E.EquipmentID AND A.OperatorID=O.OperatorID;')
        data = cursor.fetchall()
        cursor.close()

        return render_template('display_data/display_alerts_data.html', data=data)
   
# Display Operators Table
@app.route('/display_operators')
def display_operators():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT O.*, C.CompanyName FROM OPERATORS O, COMPANY C WHERE O.CompanyID=C.CompanyID;")
    data = cursor.fetchall()
    cursor.close()
    return render_template('display_data/display_operators_data.html', data=data)

# Display Energy Usage
@app.route('/display_energy_usage')
def display_energy_usage():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT E.EquipmentID, E.EquipmentName, SUM(A.EnergyConsumed) AS EnergyConsumed FROM ALERTS A , Equipments E WHERE A.EquipmentID=E.EquipmentID GROUP BY E.EquipmentID;")
    data = cursor.fetchall()
    cursor.close()
    return render_template('display_data/display_energy_usage.html', data=data)

# Display Companies
@app.route('/display_companies')
def display_companies():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM COMPANY")
    data = cursor.fetchall()
    cursor.close()
    return render_template('display_data/display_company_data.html', data=data)
    
# Selected Equipment Page rendering
@app.route('/equipment_<equipment_id>', methods=['GET', 'POST'])
def equipment_detail(equipment_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM EQUIPMENTS WHERE EquipmentID = %s', (equipment_id,))
        equipment = cursor.fetchone()

        cursor.execute("SELECT OperatorID FROM OPERATORS")
        result = cursor.fetchall()
        operators = [row['OperatorID'] for row in result]
        cursor.close()

        return render_template('equipments/equipment_detail.html', equipment=equipment, operators = operators)

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        operator_id = request.form.get('OperatorID')
        cursor.execute('INSERT INTO OPERATES (OperatorID, EquipmentID) VALUES (%s, %s)', (operator_id, equipment_id))
        mysql.connection.commit()
        
        cursor.execute('SELECT * FROM OPERATES')
        operates = cursor.fetchall()
        cursor.close()

        return render_template('display_data/display_operates_data.html', operates=operates)  

# Selected Equipment adding Alert page rendering and logic
@app.route('/equipment_<equipment_id>/add_log', methods = ['POST', 'GET'])
def add_log(equipment_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT AlertID FROM ALERTS ORDER BY AlertID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_alert_id = result['AlertID'] if result else None
        new_alert_id = increment_id(latest_alert_id)
        TimeStamp = datetime.now()
        cursor.close()

        return render_template('equipments/add_log.html', latest_alert_id = new_alert_id, equipment_id = equipment_id, time_stamp = TimeStamp)
    
    if request.method == 'POST':
        OperatorID = request.form['OperatorID']
        EnergyConsumed = request.form['EnergyConsumed']
        TimeStamp = datetime.now()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT AlertID FROM ALERTS ORDER BY AlertID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_alert_id = result['AlertID'] if result else None
        new_alert_id = increment_id(latest_alert_id)

        cursor.execute("SELECT OperatorID, EquipmentID FROM OPERATES WHERE OperatorID = %s AND EquipmentID = %s", (OperatorID, equipment_id))
        operates_check = cursor.fetchone()
        if operates_check == None:
            cursor.execute("INSERT INTO OPERATES VALUES(%s,%s)", (OperatorID, equipment_id))

        cursor.execute("INSERT INTO ALERTS VALUES(%s,%s,%s,%s,%s)",(new_alert_id, equipment_id, OperatorID, EnergyConsumed, TimeStamp))
        mysql.connection.commit()
        cursor.execute("SELECT A.*, E.EquipmentName, O.OperatorName FROM ALERTS A, EQUIPMENTS E, OPERATORS O WHERE A.EquipmentID=E.EquipmentID AND A.OperatorID=O.OperatorID;")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_data/display_alerts_data.html', data=data)


# Company Entry Page
@app.route('/company', methods = ['POST', 'GET'])
def company_entry():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT CompanyID FROM COMPANY ORDER BY CompanyID DESC LIMIT 1')
        result = cursor.fetchone()
        latest_company_id = result['CompanyID'] if result else None
        new_company_id = increment_id(latest_company_id)
        cursor.close()
        
        return render_template('forms/company.html', latest_company_id=new_company_id)
     
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
        cursor.execute("SELECT * FROM COMPANY")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_data/display_company_data.html', data=data)

# Company Data Page
@app.route('/company_data')
def display_company_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM COMPANY")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_data/display_company_data.html', data=data)
    except Exception as e:
        print("Error fetching data:", str(e))
        return "Error fetching data. Please check the console for details."
    
# Equipments Entry Page
@app.route('/equipments', methods = ['POST', 'GET'])
def equipments_entry():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT EquipmentID FROM EQUIPMENTS ORDER BY EquipmentID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_equipment_id = result['EquipmentID'] if result else None
        new_equipment_id = increment_id(latest_equipment_id)

        cursor.execute("SELECT CompanyID FROM COMPANY")
        result = cursor.fetchall()
        companies = [row['CompanyID'] for row in result]

        cursor.close()
        
        return render_template('forms/equipments.html', latest_equipment_id=new_equipment_id, companies=companies)
     
    if request.method == 'POST':
        EquipmentName = request.form['EquipmentName']
        PowerRating = request.form['PowerRating']
        ManufacturingDate = request.form['ManufacturingDate']
        CompanyID = request.form['CompanyID']        

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT EquipmentID FROM EQUIPMENTS ORDER BY EquipmentID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_equipment_id = result['EquipmentID'] if result else None
        new_equipment_id = increment_id(latest_equipment_id)

        cursor.execute(" INSERT INTO EQUIPMENTS VALUES(%s,%s,%s,%s,%s)",(new_equipment_id, EquipmentName, PowerRating, ManufacturingDate, CompanyID))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM EQUIPMENTS')
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_data/display_equipments_data.html', data=data)
    
# Equipments Data Page
@app.route('/equipments_data')
def display_equipments_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM EQUIPMENTS")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_data/display_equipments_data.html', data=data)
    except Exception as e:
        print("Error fetching data:", str(e))
        return "Error fetching data. Please check the console for details."
    
# Operators Entry Page
@app.route('/operators', methods = ['POST', 'GET'])
def operators_entry():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT OperatorID FROM OPERATORS ORDER BY OperatorID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_operator_id = result['OperatorID'] if result else None
        new_opeator_id = increment_id(latest_operator_id)
        
        cursor.execute("SELECT CompanyID FROM COMPANY")
        result = cursor.fetchall()
        companies = [row['CompanyID'] for row in result]
        
        cursor.close()

        return render_template('forms/operators.html', latest_operator_id=new_opeator_id, companies=companies)
     
    if request.method == 'POST':
        OperatorName = request.form['OperatorName']
        Occuption = request.form['Occupation']
        PhoneNumber = request.form['PhoneNumber']
        CompanyID = request.form['CompanyID']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT OperatorID FROM OPERATORS ORDER BY OperatorID DESC LIMIT 1")
        result = cursor.fetchone()
        latest_operator_id = result['OperatorID'] if result else None
        new_opeator_id = increment_id(latest_operator_id)

        cursor.execute("INSERT INTO OPERATORS VALUES(%s,%s,%s,%s,%s)",(new_opeator_id, OperatorName, Occuption, PhoneNumber, CompanyID))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM OPERATORS')
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_data/display_operators_data.html', data=data)
    
# Operators Data Page
@app.route('/operators_data')
def display_operators_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM OPERATORS")
        data = cursor.fetchall()
        cursor.close()
        return render_template('display_data/display_operators_data.html', data=data)
    except Exception as e:
        print("Error fetching data:", str(e))
        return "Error fetching data. Please check the console for details."

# Function to increment the retrieved IDs
def increment_id(id):
    prefix = id[:-3]
    num = id[-3:]

    num = int(num) + 1
    num = str(num).zfill(3)

    return prefix + num

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
