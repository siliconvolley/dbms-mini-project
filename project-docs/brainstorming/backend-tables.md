# Tables for the Database

    Company:
        Attributes:
            CompanyID (Primary Key)
            CompanyName
            Location
            Contact

        Relations:
            Company Owns Equipments -> 1:N Relationship

    Equipment:
        Attributes:
            EquipmentID (Primary Key)
            EquipmentName
            PowerRating
            ManufacturingDate
            CompanyID (Foreign Key from Company)

        Relations:
            Equipment Alerts Operators -> 1:1 Relationship

    Operators:
        Attributes:
            OperatorID (Primary Key)
            OperatorName
            Occupation
            PhoneNumber
            CompanyID (Foreign Key from Company)

        Relations:
            Operator Operates Equipment -> M:N Relationship
            Operator Works_For Company -> N:1 Relationship


    Alerts (Created from 1:1 Relation between Equipments & Operators):
        Attributes:
            EquipmentID (Primary Key)
            OperatorID (Primary Key)
            EnergyConsumed
            TimeStamp

    Operates (Created from M:N Relation between Equipments & Operators):
        Attributes:
            OperatorID (Primary Key)
            CompanyID (Primary Key)


<div style="text-align: center; text-decoration: underline; margin-top: 5rem">
    <h3 style="margin: 0;">ER Diagram</h3>
    <img src="../ER.png" alt="ER Diagram" style="scale: 0.8; margin-bottom: 0;">
    <h3 style="margin: 0;">Relational Schema</h3>
    <img src="../SCHEMA (2).png" alt="ER Diagram" style="scale: 0.8;">
</div>