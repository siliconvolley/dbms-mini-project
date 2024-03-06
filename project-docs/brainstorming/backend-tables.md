# Database Requirements

<div style="text-align: center; text-decoration: underline; margin-top: 5rem">
    <h3 style="margin: 0;">ER Diagram</h3>
    <img src="../ER.png" alt="ER Diagram" style="scale: 0.8; margin-bottom: 0;">
    <h3 style="margin: 0;">Relational Schema</h3>
    <img src="../SCHEMA-2.png" alt="ER Diagram" style="scale: 0.8;">
</div>

## Table Creation 

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
    OperatorID varchar(10),
    CompanyID varchar(10),
    PRIMARY KEY (OperatorID, CompanyID),
    FOREIGN KEY (OperatorID) REFERENCES OPERATORS(OperatorID),
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
);
```