DROP DATABASE IF EXISTS MoneyTracker;
CREATE DATABASE MoneyTracker;
USE MoneyTracker;
CREATE TABLE prihodi(
IDprihodi int NOT NULL AUTO_INCREMENT PRIMARY KEY,
kategorije varchar(255) NOT NULL,
opis varchar(255),
iznos varchar(255) NOT NULL,
datumVrijeme datetime DEFAULT NOW()
);
CREATE TABLE rashodi(
IDrashodi int NOT NULL AUTO_INCREMENT PRIMARY KEY,
kategorije varchar(255) NOT NULL,
opis varchar(255),
iznos varchar(255) NOT NULL,
datumVrijeme datetime default NOW()
)ENGINE=InnoDB;

