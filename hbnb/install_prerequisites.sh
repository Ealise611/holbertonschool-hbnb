#!/bin/bash

apt update
apt install mysql-server
service mysql start

pip install -r requirements.txt 

# Login to MySQL as root
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS hbnb_db;"
