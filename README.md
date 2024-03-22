# DBMS Mini Project (Energy Monitoring System)

Description: A Python and MySQL project for tracking electrical equipment, operators, and energy consumption. Enables companies to manage equipment ownership, monitor energy usage, and generate alerts. Includes relational database schema, backend implemented in Python using Flask, and MySQL. Promotes efficient resource optimization and sustainability practices within organizations

<div style="text-align: center; text-decoration: underline; margin-top: 5rem; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: center; margin-right: 1rem;">
        <img src="/project-docs/ER.png" alt="ER Diagram" style="width: 80%; height: 400px; object-fit: contain; margin-bottom: 0;">
        <h3 style="margin: 0;">ER Diagram</h3>
    </div>
    <div style="display: flex; flex-direction: column; align-items: center;">
        <img src="/project-docs/SCHEMA-final.png" alt="Relational Schema" style="width: 80%; height: 400px; object-fit: contain;">
        <h3 style="margin: 0;">Relational Schema</h3>
    </div>
</div>

## Requirements
1. Make sure that the following are installed:
    - [Python](https://www.python.org/downloads/)
    - [MySQL](https://www.mysql.com/downloads/)

2. Setting up the local database:
    - Run MySQL in your terminal:

    ```
    mysql -u root -p
    ```

    - Enter your password
    - **NOTE**: Update your MySQL password in the `config.py` file
    - Create the database called `dbms_mp_1`

    ```
    CREATE DATABASE dbms_mp_1;
    ```

    - Create the following tables:
    
    ```
    CREATE TABLE COMPANY (
        CompanyID varchar(10),
        CompanyName varchar(20),
        Location varchar(15),
        Contact integer,
        PRIMARY KEY (CompanyID)
    );
    ```
    ```
    CREATE TABLE EQUIPMENTS (
        EquipmentID varchar(10),
        EquipmentName varchar(20),
        PowerRating integer,
        ManufacturingDate date,
        CompanyID varchar(10),
        PRIMARY KEY (EquipmentID),
        FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
    );
    ```
    ```
    CREATE TABLE OPERATORS (
        OperatorID varchar(10),
        OperatorName varchar(20),
        Occupation varchar(15),
        PhoneNumber integer,
        CompanyID varchar(10),
        PRIMARY KEY (OperatorID),
        FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
    );
    ```
    ```
    CREATE TABLE ALERTS (
        EquipmentID varchar(10),
        OperatorID varchar(10),
        EnergyConsumed integer,
        TimeStamp timestamp,
        PRIMARY KEY (EquipmentID, OperatorID),
        FOREIGN KEY (EquipmentID) REFERENCES EQUIPMENTS(EquipmentID),
        FOREIGN KEY (OperatorID) REFERENCES OPERATORS(OperatorID)
    );
    ```
    ```
    CREATE TABLE OPERATES (
        OperatorID varchar(20),
        EquipmentID varchar(20),
        PRIMARY KEY (OperatorID, EquipmentID),
        FOREIGN KEY (OperatorID) REFERENCES OPERATORS(OperatorID),
        FOREIGN KEY (EquipmentID) REFERENCES EQUIPMENTS(EquipmentID)
    );
    ```
    ```
    CREATE TABLE AUTH (
        UserName varchar(30),
        Password varchar(30),
        PRIMARY KEY (UserName, Password)
    );
    ```

## Installation (Run this locally)

1. Clone this repo:
```
git clone https://github.com/siliconvolley/dbms-mini-project.git
```
2. Install the dependencies:
```
pip install -r requirements.txt
```
3. Run the app:
```
python main.py
```
