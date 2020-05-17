DROP DATABASE IF EXISTS ZooAtl;
CREATE DATABASE ZooAtl;
	USE ZooAtl;

DROP TABLE IF EXISTS user;
CREATE TABLE user (
	username varchar(50) PRIMARY KEY,
	password varchar(50) NOT NULL CHECK (LEN(password) >= 8),
	email varchar(50) NOT NULL UNIQUE CHECK (email LIKE '%_@__%.__%'),
	role varchar(10) NOT NULL
);

DROP TABLE IF EXISTS adminUser;
CREATE TABLE adminUser (
	username varchar(50),

	FOREIGN KEY (username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS staff;
CREATE TABLE staff (
	username varchar(50),

	FOREIGN KEY (username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS visitor;
CREATE TABLE visitor (
	username varchar(50),

	FOREIGN KEY (username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS exhibit;
CREATE TABLE exhibit (
	exhibitName varchar(50),
	waterFeature boolean,
	size int,

	PRIMARY KEY (exhibitName)
);


DROP TABLE IF EXISTS animal;
CREATE TABLE animal (
	animalName varchar(50),
	animalSpecies varchar(50),
	type_ varchar(20) NOT NULL,
	age int NOT NULL,
	exhibitName varchar(50),

	PRIMARY KEY (animalName, animalSpecies),
	FOREIGN KEY (exhibitName) REFERENCES exhibit(exhibitName) ON UPDATE CASCADE ON DELETE CASCADE
);



DROP TABLE IF EXISTS show_;
CREATE TABLE show_ (
	showName varchar(50),
	dateAndTime varchar(20) NOT NULL UNIQUE CHECK (dateandtime LIKE '%M/%D/%Y %H:%M %_M'),
	username varchar(50),
	exhibitName varchar(50),

	PRIMARY KEY (showName, dateAndTime),
	FOREIGN KEY (username) REFERENCES staff(username) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (exhibitName) REFERENCES exhibit(exhibitName) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS AnimalCare;
CREATE TABLE AnimalCare (
	animalName varchar(50),
	animalSpecies varchar(50),
	username varchar(50),
	dateandtime varchar(20) NOT NULL UNIQUE CHECK (dateandtime LIKE '%M/%D/%Y %H:%M %_M'),
	notetext TEXT NOT NULL,

	PRIMARY KEY (animalName, animalSpecies, username, dateandtime),
	FOREIGN KEY (username) REFERENCES staff(username) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (animalName, animalSpecies) REFERENCES animal(animalName, animalSpecies) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS exhibitvisitor;
CREATE TABLE exhibitvisitor (
	username varchar(50),
	exhibitName varchar(50),
	dateandtime varchar(20) NOT NULL UNIQUE CHECK (dateandtime LIKE '%M/%D/%Y %H:%M %_M'),

	FOREIGN KEY (username) REFERENCES visitor(username) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (exhibitName) REFERENCES exhibit(exhibitName) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS showvisitor;
CREATE TABLE showvisitor (
	username varchar(50),
	showName varchar(50),
	dateandtime varchar(20) NOT NULL UNIQUE CHECK (dateandtime LIKE '%M/%D/%Y %H:%M %_M'),

	FOREIGN KEY (username) REFERENCES visitor(username) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (showName) REFERENCES show_(showName) ON UPDATE CASCADE ON DELETE CASCADE
);


