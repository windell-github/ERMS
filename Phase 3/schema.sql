DROP USER IF EXISTS 'gatechUser'@'localhost';
CREATE USER 'gatechUser'@'localhost' IDENTIFIED BY 'gatech123';
DROP DATABASE IF EXISTS `cs6400_su18_team039`;
SET default_storage_engine=InnoDB;
CREATE DATABASE IF NOT EXISTS cs6400_su18_team039;
USE cs6400_su18_team039;
GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON cs6400_su18_team039.* TO 'gatechUser'@'localhost';

FLUSH PRIVILEGES;
#Tables
# user tables
CREATE TABLE User (
    username VARCHAR(250) NOT NULL,
    PRIMARY KEY (username), 
    name VARCHAR(250) NOT NULL,
    password VARCHAR(250) NOT NULL
);
CREATE TABLE Individual (
    username VARCHAR(250) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES User(username),
    job_title VARCHAR(250) NOT NULL,
    hire_date DATETIME NOT NULL  
);
CREATE TABLE GovernmentAgency (
    username VARCHAR(250) NOT NULL,    
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES User(username),
    local_office VARCHAR(250) NOT NULL,
    agency_name VARCHAR(250) NOT NULL  
);
CREATE TABLE Municipality (
    username VARCHAR(250) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES User(username),
    category VARCHAR(250) NOT NULL
);
CREATE TABLE Company (
    username VARCHAR(250) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES User(username),
    number_of_employees INT NOT NULL, 
    headquarters VARCHAR(250) NOT NULL  
);
#Incident tables
CREATE TABLE Declaration (
    declaration_type INT NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (declaration_type),
    declaration_description VARCHAR(250) NOT NULL,
    declaration_abbreviation varchar(3) not null
);


#change the id line from INT to VARCHAR(50)
    CREATE TABLE Incident (
	id VARCHAR(50) NOT NULL,        
	PRIMARY KEY (id), 
        #CONSTRAINT PK_Incident PRIMARY KEY (id, declaration),
        owner VARCHAR(250) NOT NULL,
        FOREIGN KEY (owner) REFERENCES User(username),
        description VARCHAR(250),
        date DATETIME NOT NULL,
        declaration INT, 
        FOREIGN KEY (declaration) REFERENCES Declaration(declaration_type),
        location_latitude DECIMAL(10,4) NOT NULL,
        location_longitude DECIMAL(10,4) NOT NULL
    );

#Resources tables
CREATE TABLE CostPer (
    PRIMARY KEY (unit_of_measure),
    unit_of_measure VarChar(50) NOT NULL
);
CREATE TABLE Cost (
    cost_id Int NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (cost_id),
    amount decimal(10,4) NOT NULL,
    unit_of_measure varchar(50),
    Foreign Key (unit_of_measure) References CostPer(unit_of_measure)
);
CREATE TABLE ESF (
    esf_designation INT NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (esf_designation),
    esf_description VARCHAR(250) NOT NULL
);
    
    CREATE TABLE Resource (
        id INT NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (id),
        owner VARCHAR(250) NOT NULL,
        FOREIGN KEY (owner) REFERENCES User(username),
        name VARCHAR(50) NOT NULL,
        status varchar(50) NOT NULL,
        max_distance INT,
        model varchar(50),
        home_location_latitude DECIMAL(10,4) NOT NULL,
        home_location_longitude DECIMAL(10,4) NOT NULL,
        cost_id INT,
        FOREIGN KEY (cost_id) REFERENCES Cost(cost_id),
        esf_primary_designation int NOT NULL,
        FOREIGN KEY (esf_primary_designation) REFERENCES ESF(esf_designation)
    );

CREATE TABLE ResourceCapability (
    id INT NOT NULL, 
    Foreign Key (id) References Resource(id),
    capability VARCHAR(250) NOT NULL
);
CREATE TABLE HasSecondaryESFDesignation(
    id INT NOT NULL,
    Foreign Key (id) References Resource(id),
    esf_designation INT NOT NULL,
    FOREIGN KEY (esf_designation) REFERENCES ESF(esf_designation)
);
    
#change Foreign keys to VARCHAR because Incident(id) was changed.
Create Table Deployed (
    id_incident VARCHAR(50) not null,
    FOREIGN KEY (id_incident) REFERENCES Incident(id),
    id_resource int not null,
    FOREIGN KEY (id_resource) REFERENCES Resource(id),
    date_deployed DateTime,
    actual_return_date DateTime
);
   
Create Table Request (
    username VARCHAR(250) not null,
    FOREIGN KEY (username) REFERENCES User(username),
    id_incident VARCHAR(50) not null,
    FOREIGN KEY (id_incident) REFERENCES Incident(id),
    id_resource int not null,
    FOREIGN KEY (id_resource) REFERENCES Resource(id),
    expected_return_date DateTime
);

#inserting start information. 
insert into User values ('kyle', 'Kyle Bechtel', 'password');
insert into User values ('alex', 'Alex OSullivan', 'password');
insert into User values ('brian', 'Brian Beck', 'password');
insert into User values ('windell', 'Windell', 'password');
#testing the main page, run these one at a time and reload the main page each time. 
insert into Municipality values ('kyle', 'City of Gotham');
insert into Company values ('alex', 2400, 'Wayne Enterprises');
insert into GovernmentAgency values ('brian', 'Atlanta', 'CDCP');
insert into Individual values ('windell','database admin',STR_TO_DATE( '11/16/1996 18:33:55', '%m/%d/%Y %H:%i:%s'));
insert into Declaration (declaration_description, declaration_abbreviation) values('Major Disaster','MD');
insert into Declaration (declaration_description, declaration_abbreviation) values('Emergency','ED');
insert into Declaration (declaration_description, declaration_abbreviation) values('Fire Management Assistance','FM');
insert into Declaration (declaration_description, declaration_abbreviation) values('Fire Suppression Authorization','FS');

insert into ESF values(1, 'Transportation');
insert into ESF values(2, 'Communications');
insert into ESF values(3, 'Public Works and Engineering');
insert into ESF values(4, 'Firefighting');
insert into ESF values(5, 'Emergency Management');
insert into ESF values(6, 'Mass Care, Emergency Assistance, Housing, and Human Services');
insert into ESF values(7, 'Logistics Management and Resource Support');
insert into ESF values(8, 'Public Health and Medical Services');
insert into ESF values(9, 'Search and Rescue');
insert into ESF values(10, 'Oil and Hazardous Materials Response');
insert into ESF values(11, 'Agriculture and Natural Resources');
insert into ESF values(12, 'Energy');
insert into ESF values(13, 'Public Safety and Security');
insert into ESF values(14, 'Long-Term Community Recovery');
insert into ESF values(15, 'External Affairs');

insert into CostPer values ('Hour');
insert into CostPer values ('Day');
insert into CostPer values ('Week');
insert into CostPer values ('Each');

insert into Cost values (1,50.00,'Hour');
insert into Cost values (2,100,'Each');
insert into Cost values (3,300,'Day');
insert into Cost values (4,1500,'Week');

#alex's starting resources
insert into Resource values (1,'alex','Leo''s Ladder','AVAILABLE',null,'modelA',33.82, -84.34,1,1);
insert into ResourceCapability values (1, 'Atlanta');
insert into Resource values (2, 'alex', 'Will''s Little Giant','AVAILABLE',500,'Ladder',33.82, -84.34,2,2);
insert into ResourceCapability values (2, 'Atlanta');
insert into Resource values (3,'alex','Peter''s Fire Truck','AVAILABLE',500,'unique',33.82, -84.34,3,3);
insert into ResourceCapability values (3, 'Atlanta');
insert into ResourceCapability values (3, 'Ladder');
insert into Resource values (4, 'alex', 'snow blower','AVAILABLE',500,'Honda 33M (5hp)',33.82, -84.34,4,4);
insert into ResourceCapability values (4, 'Atlanta');


#windell's starting resources
insert into Resource values (5,'windell','Windell Resource 1','AVAILABLE',null,'model5',33.95,-84.55,1,5);
insert into ResourceCapability values (5, 'Marietta');
insert into Resource values (6, 'windell', 'Windell Resource 2','AVAILABLE',500,'model6',33.95,-84.55,2,6);
insert into ResourceCapability values (6, 'Marietta');
insert into Resource values (7,'windell','Windell Resource 3','AVAILABLE',500,'model7',33.95,-84.55,3,7);
insert into ResourceCapability values (7, 'Marietta');
insert into Resource values (8, 'windell', 'Windell Resource 4','AVAILABLE',500,'model8',33.95,-84.55,4,8);
insert into ResourceCapability values (8, 'Marietta');




#brians's starting resources
insert into Resource values (9,'brian','Brian Resource 1','AVAILABLE',null,'model9',30.30,-97.73,1,9);
insert into ResourceCapability values (9, 'Austin');
insert into Resource values (10, 'brian', 'Brian Resource 2','AVAILABLE',null,'model10',30.30,-97.73,2,10);
insert into ResourceCapability values (10, 'Austin');
insert into Resource values (11,'brian','Brian Resource 3','AVAILABLE',500,'model11',30.30,-97.73,3,11);
insert into ResourceCapability values (11, 'Austin');
insert into Resource values (12, 'brian', 'Brian Resource 4','AVAILABLE',500,'model12',30.30,-97.73,4,12);
insert into ResourceCapability values (12, 'Austin');


#kyle's starting resources
insert into Resource values (13,'kyle','Kyle Resource 1','AVAILIBLE',null,'model9',34.05,-84.10,1,13);
insert into ResourceCapability values (13, 'Suwanee');
insert into Resource values (14, 'kyle', 'Kyle Resource 2','AVAILABLE',500,'model10',34.05,-84.10,2,14);
insert into ResourceCapability values (14, 'Suwanee');
insert into Resource values (15,'kyle','Kyle Resource 3','AVAILABLE',500,'model11',34.05,-84.10,3,15);
insert into ResourceCapability values (15, 'Suwanee');
insert into Resource values (16, 'kyle', 'Kyle Resource 4','AVAILABLE',500,'model12',34.05,-84.10,4,1);
insert into ResourceCapability values (16, 'Suwanee');



#alex Incidents
insert into Incident values ('MD-1', 'alex', 'Stone Mountain Major Disaster', curdate(), 1, 33.81,  -84.17);
insert into Incident values ('ED-1', 'alex', 'Stone Mountain Emergency ', curdate(), 2, 33.81,  -84.17);
insert into Request values ('alex', 'MD-1', 7, '2018-07-30');
UPDATE Resource SET status = "IN USE" WHERE id = 7;
insert into Deployed values ('MD-1', 7, '2018-07-10', null);
insert into Request values ('alex', 'ED-1', 9, '2018-07-30');
#alex Requests

#windell incidents
insert into Incident values ('FM-1', 'windell', 'The Varsity Fire Management', curdate(), 3, 33.77,  -84.30);
insert into Incident values ('FS-1', 'windell', 'The Varsity Fire Supression', curdate(), 4, 33.77,  -84.30);
insert into Request values ('windell', 'FM-1', 2, '2018-07-30');
UPDATE Resource SET status = "IN USE" WHERE id = 2;
insert into Deployed values ('FM-1', 2, '2018-07-10', null);
insert into Request values ('windell', 'FS-1', 14, '2018-07-30');

#brian incidents
insert into Incident values ('MD-2', 'brian', 'Waco Major Disaster', curdate(), 1, 31.55, -97.15);
insert into Incident values ('ED-2', 'brian', 'Waco Emergency', curdate(), 2, 31.55, -97.15);

insert into Request values ('brian', 'MD-2', 13, '2018-07-30');
UPDATE Resource SET status = "IN USE" WHERE id = 13;
insert into Deployed values ('MD-2', 13, '2018-07-10', null);
insert into Request values ('brian', 'ED-2', 5, '2018-07-30');


#kyle incidents
insert into Incident values ('FM-2', 'kyle', 'UGA Fire Management', curdate(), 3, 33.95, -83.38);
insert into Incident values ('FS-2', 'kyle', 'UGA Fire Supression', curdate(), 4, 33.95, -83.38);
insert into Request values ('kyle', 'FM-2', 10, '2018-07-30');
UPDATE Resource SET status = "IN USE" WHERE id = 10;
insert into Deployed values ('FM-2', 10, '2018-07-10', null);
insert into Request values ('kyle', 'FS-2', 1, '2018-07-30');


#    INSERT INTO Incident (id, description, date, owner, location_latitude, location_longitude, declaration)
#    VALUES (@IdPhrase, '$description', '$date', '$username', '$long', '$lat', @DeclarationType);

#SELECT declaration_description, declaration_abbreviation FROM Declaration;
#Select * from Incident;
#    SET @DeclarationType = (SELECT declaration_type FROM Declaration WHERE Declaration.declaration_description = '$declaration');
#    SET @IdNumber = (SELECT id from Incident WHERE Incident.declaration = 1 ORDER BY id DESC Limit 1);
#    Set @IdNumber = If(@IdNumber Is Null, 0, @IdNumber);
#    SET @IdNumber = @IdNumber + 1;
#    SET @IdPhrase = CONCAT(@DeclarationType, " ", @IdNumber);

