CREATE USER `gatechUser@localhost` IDENTIFIED BY 'gatech123';

DROP DATABASE IF EXISTS `cs6400_su18_team039`;
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_su18_team039
	DEFAULT CHARACTER SET utf8mb4
	DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_su18_team039;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 
'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_su18_team039`.* TO 
'gatechUser'@'localhost';
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
	FOREIGN KEY (username) REFERENCES User(username),
	job_title VARCHAR(250) NOT NULL,
	hire_date DATETIME NOT NULL  
);

CREATE TABLE GovernmentAgency (
	username VARCHAR(250) NOT NULL,
	FOREIGN KEY (username) REFERENCES User(username),
	local_office VARCHAR(250) NOT NULL,
	agency_name VARCHAR(250) NOT NULL  
);

CREATE TABLE Municipality (
	username VARCHAR(250) NOT NULL,
	FOREIGN KEY (username) REFERENCES User(username),
	category VARCHAR(250) NOT NULL
);

CREATE TABLE Company (
	username VARCHAR(250) NOT NULL,
	FOREIGN KEY (username) REFERENCES User(username),
	number_of_employees INT NOT NULL, 
	headquarters VARCHAR(250) NOT NULL  
);

#Incident tables
CREATE TABLE Declaration (
	declaration_type INT NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (declaration_type),
	declaration_description VARCHAR(250) NOT NULL
);

	CREATE TABLE Incident (
		id INT NOT NULL AUTO_INCREMENT, 
		CONSTRAINT PK_Incident PRIMARY KEY (id,declaration),
		owner VARCHAR(50) NOT NULL,
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
		model VARCHAR(50) NOT NULL,
		cost_id INT,
        status varchar(50) NOT NULL,
		FOREIGN KEY (cost_id) REFERENCES Cost(cost_id),
		owner VARCHAR(50) NOT NULL,
		FOREIGN KEY (owner) REFERENCES User(username),
		name VARCHAR(50) NOT NULL,
		esf_primary_designation int NOT NULL,
   		FOREIGN KEY (esf_primary_designation) REFERENCES ESF(esf_designation),
		max_distance INT,
		home_location_latitude DECIMAL(10,4) NOT NULL,
		home_location_longitude DECIMAL(10,4) NOT NULL
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
    
Create Table Deployed (
	id_incident int not null,
	FOREIGN KEY (id_incident) REFERENCES Incident(id),
	id_resource int not null,
	FOREIGN KEY (id_resource) REFERENCES Resource(id),
    date_deployed DateTime,
    actual_return_date DateTime
);
   
Create Table Request (
	username VARCHAR(250) not null,
	FOREIGN KEY (username) REFERENCES User(username),
	id_incident int not null,
	FOREIGN KEY (id_incident) REFERENCES Incident(id),
	id_resource int not null,
	FOREIGN KEY (id_resource) REFERENCES Resource(id),
    expected_return_date DateTime
);
