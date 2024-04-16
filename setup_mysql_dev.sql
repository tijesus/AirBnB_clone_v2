-- Creating Databe for the project
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Creating user database with password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Giving all database permission to user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Reloading the database after granting permision
FLUSH PRIVILEGES;
-- Giving all performance schema permissions to user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
-- Reloading the database after granting permision
FLUSH PRIVILEGES;
