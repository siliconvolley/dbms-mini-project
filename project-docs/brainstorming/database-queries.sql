
DROP TABLE OPERATES;
DROP TABLE ALERTS;
DROP TABLE OPERATORS;
DROP TABLE EQUIPMENTS;
DROP TABLE COMPANY;

---TABLE CREATION---

CREATE TABLE COMPANY (
    CompanyID varchar(20),
    CompanyName varchar(30),
    Location varchar(30),
    Contact integer,
    PRIMARY KEY (CompanyID)
);

CREATE TABLE EQUIPMENTS (
    EquipmentID varchar(20),
    EquipmentName varchar(30),
    PowerRating integer,
    ManufacturingDate date,
    CompanyID varchar(20),
    PRIMARY KEY (EquipmentID),
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
);

CREATE TABLE OPERATORS (
    OperatorID varchar(20),
    OperatorName varchar(30),
    Occupation varchar(20),
    PhoneNumber integer,
    CompanyID varchar(20),
    PRIMARY KEY (OperatorID),
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
);

CREATE TABLE ALERTS (
    EquipmentID varchar(20),
    OperatorID varchar(20),
    EnergyConsumed integer,
    TimeStamp timestamp,
    PRIMARY KEY (EquipmentID, OperatorID),
    FOREIGN KEY (EquipmentID) REFERENCES EQUIPMENTS(EquipmentID),
    FOREIGN KEY (OperatorID) REFERENCES OPERATORS(OperatorID)
);

CREATE TABLE OPERATES (
    OperatorID varchar(20),
    CompanyID varchar(20),
    PRIMARY KEY (OperatorID, CompanyID),
    FOREIGN KEY (OperatorID) REFERENCES OPERATORS(OperatorID),
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
);

---DATA INSERTION---
INSERT INTO COMPANY (CompanyID, CompanyName, Location, Contact)
VALUES 
    ('C001', 'ABC Electronics', 'New York', 1234567890),
    ('C002', 'XYZ Tech', 'San Francisco', 9876543210),
    ('C003', 'Tech Innovators', 'London', 4567890123),
    ('C004', 'Global Systems', 'Tokyo', 7890123456),
    ('C005', 'Smart Solutions', 'Sydney', 3210987654);

INSERT INTO EQUIPMENTS (EquipmentID, EquipmentName, PowerRating, ManufacturingDate, CompanyID)
VALUES 
    ('E001', 'Generator X', 1000, '2022-02-15', 'C001'),
    ('E002', 'Robotics Arm', 500, '2021-08-10', 'C002'),
    ('E003', 'Solar Panel System', 200, '2023-05-20', 'C003'),
    ('E004', 'Industrial Printer', 800, '2022-11-05', 'C004'),
    ('E005', 'HVAC System', 300, '2023-01-30', 'C005');

INSERT INTO OPERATORS (OperatorID, OperatorName, Occupation, PhoneNumber, CompanyID)
VALUES 
    ('O001', 'John Smith', 'Technician', 5551234567, 'C001'),
    ('O002', 'Emily White', 'Engineer', 5559876543, 'C002'),
    ('O003', 'David Brown', 'Operator', 5552345678, 'C003'),
    ('O004', 'Sarah Miller', 'Maintenance', 5558765432, 'C004'),
    ('O005', 'Alex Johnson', 'Inspector', 5553456789, 'C005');

INSERT INTO ALERTS (EquipmentID, OperatorID, EnergyConsumed, TimeStamp)
VALUES 
    ('E001', 'O001', 1500, '2024-03-05 08:30:00'),
    ('E002', 'O002', 800, '2024-03-05 10:15:00'),
    ('E003', 'O003', 300, '2024-03-05 12:45:00'),
    ('E004', 'O004', 1200, '2024-03-05 14:30:00'),
    ('E005', 'O005', 500, '2024-03-05 16:00:00');

INSERT INTO OPERATES (OperatorID, CompanyID)
VALUES 
    ('O001', 'C001'),
    ('O002', 'C002'),
    ('O003', 'C003'),
    ('O004', 'C004'),
    ('O005', 'C005');

SELECT * FROM COMPANY;
SELECT * FROM EQUIPMENTS;
SELECT * FROM OPERATORS;
SELECT * FROM ALERTS;
SELECT * FROM OPERATES;

