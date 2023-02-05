""" required connectors
pip install mysql-connector
pip install mysql-connector-python
pip install mysql-connector-python-rf

"""
# create db 
import mysql.connector
from classified import passwd, user


mydb = mysql.connector.connect(
    host="localhost",
    user=user,
    passwd=passwd
    )


mycursor = mydb.cursor()  
mycursor.execute("USE NBP")

