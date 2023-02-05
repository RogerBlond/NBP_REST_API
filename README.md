# NBP DB - Python flask REST API based on data from National Bank of Poland

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info

This project is simply REST API interface able to fetching data from NBP API to local database (MySQL) and manage url requests(GET,POST,PUT,DELETE) for future web aplication. During this project I learned REST API concept, Flask basics and connecting API to local db.
	
## Technologies
Project is created with:
* Python version: 3.11
    * Flask version: 2.2.2
    * Flask_RESTful: 0.3.9
    * Flask_SQLAlchemy: 3.0.2
    * SQLAlchemy: 1.4.46
    * requests: 2.28.1
    * mysql_connector: 2.2.9
    * mysql_connector_python: 8.0.31
    * pandas: 1.5.1
    * PyMySQL: 1.0.2
* MySQL database version: 8.0.31

## Setup
To run this project, install:
* required connectors:
```
    $ pip install mysql-connector
    $ pip install mysql-connector-python
    $ pip install mysql-connector-python-rf
```

* and connect to DB using shell commands( or launch db_shell.py):
```
    $from app import app,db
    $app.app_context().push()
    $db.create_all()
```
after db.create_all() command these errors may occured:
- error: "no module called 'mySQLdb'" ---> solution: 
    pip install pymysql
    pip install cryptography
    add +pymysql to path in SQLALCHEMY_DATABASE_URI

- error: working outside of app context ---> solution:
    app.app_context().push() 

## The project status
The project is still being developed and gonna be transformed in full web service. Enjoy ;)

