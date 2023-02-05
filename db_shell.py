import mysql.connector
from connectors import mydb
from app import app, db, Table_A

mycursor = mydb.cursor()  

#execute only first time
mycursor.execute("CREATE DATABASE NBP")

mycursor.execute("USE NBP")

app.app_context().push()
db.create_all()
emp = Table_A(time="test-tt-tt",code="Test",currency="TST",mid="1")
db.session.add(emp)
db.session.commit()

