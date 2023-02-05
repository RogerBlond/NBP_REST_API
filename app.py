from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import requests, json
import mysql.connector  #it can be replaced by dataframe from pandas
from datetime import date, timedelta
import pandas as pd
from connectors import mydb 
from classified import passwd, user
app = Flask(__name__)           #create instance of flask
api = Api(app)          #create instance of API to url routing

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/name'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{passwd}@localhost/nbp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # instance of sqlalchemy to interact with db


class Table_A(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    time = db.Column(db.String(80))
    code = db.Column(db.String(80))
    currency = db.Column(db.String(80))
    mid = db.Column(db.Float)

    def __repr__(self):          #represent a class’s objects as a string, this is represantation of class Table_A as a string
        return f"{self.id} - {self.time} - {self.code} - {self.currency} - {self.mid}"




@app.route('/fetch', methods=['GET']) 
def fetch():
    start_date = date.today() - timedelta(days=92)
    end_date = date.today()
    
    for n in range(int((end_date - start_date).days)):
        loop_date = start_date + timedelta(n)
        yield str(loop_date)    #coversion to str needed in generator 
        #print(loop_date)
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/a/{}/{}/".format(start_date, end_date))
            
        data = json.loads(response.content.decode('utf-8'))

        mycursor = mydb.cursor()  #to interact with the connection 

        #here i should check in future if theres no package from the same time
        db_data=[]
        for d in data:
            for r in d['rates']:
                tupple = (d['effectiveDate'],r['code'],r['currency'],r['mid'])
                db_data.append(tupple)
                
                sql = "INSERT INTO table_a (time,code, currency, mid) VALUES (%s,%s, %s, %s)"
                val = (d['effectiveDate'],r['code'],r['currency'],r['mid'])
                mycursor.execute(sql, val)
                mydb.commit()
                
        mydb.close()
        return {"Data fetched from last 92 days": db_data,},200 

#for GET request to http://127.0.0.1:6666/get   
@app.route('/get', methods=['GET']) 
def get():
    results = Table_A.query.all()
    row_list = []
    for row in results:
        data = {'id':row.id, 'time':row.time, 'code':row.code, 'currency':row.currency, 'mid':row.mid}
        row_list.append(data)
    return {"Results": row_list,},200



#for POST request to http://127.0.0.1:6666/post   
@app.route('/post', methods=['POST']) 
def post():
    if request.is_json:
        row = Table_A(time=request.json['time'], code=request.json['code'],
                currency=request.json['currency'],mid=request.json['mid'])
        db.session.add(row)
        db.session.commit()

        return make_response(jsonify({'id':row.id, 'time':row.time, 'code':row.code, 'currency':row.currency, 'mid':row.mid}),201)
    else:
        return{'ERROR': 'Request must be in JSON format'},400

#for PUT request to http://127.0.0.1:6666/put/  
@app.route('/put/<int:id>', methods=['PUT']) 
def put(id):
    if request.is_json:
        row = Table_A.query.get(id)
        if row is None:
            return{'ERROR': 'No found'},404
        else:
            row.time=request.json['time']
            row.code=request.json['code']
            row.currency=request.json['currency']
            row.mid=request.json['mid']
            db.session.commit()
            return 'Updated',200
    else:
        return{'ERROR': 'Request must be in JSON format'},400

#for DELETE request to http://127.0.0.1:6666/delete/  
@app.route('/delete/<int:id>', methods=['DELETE']) 
def delete(id):
    row = Table_A.query.get(id)
    if row is None:
        return{'ERROR': 'No found'},404
    else:
        db.session.delete(row)
        db.session.commit()
        return f'Row with id:{id} was deleted',200
    

#for DELETE duplicates to http://127.0.0.1:6666/delete/  
@app.route('/dd', methods=['DELETE']) 
def delete_duplicates():
    mycursor = mydb.cursor(buffered=True)
    condition ="SELECT COUNT(*) FROM Table_a GROUP BY time,code,currency,mid HAVING COUNT(*) > 1;"
    mycursor.execute(condition)
    result = mycursor.fetchone()
    #print(f'Result: {result[0]}') jak policzyc ilosc rekordow
    if result == 0:
        return{'ERROR': 'No duplicates found in database'},404
    else:
        #HINT: MySQL syntax does not let you assign an alias to a select query when it is part of an update statement.  So we have to put it inside another query which, I suppose separates it from the update statement.
        sqlstr = """DELETE FROM Table_A WHERE ID NOT IN (SELECT * FROM (SELECT MAX(ID) AS MaxID FROM Table_A GROUP BY time,code, currency, mid)temp);"""
        mycursor.execute(sqlstr)
        mydb.commit()
        mydb.close()
        return 'Rows deleted!',200
    


#create instance of API to url routing
if __name__== "__main__":
    app.run(debug=True,port=6666)


# wzór https://www.youtube.com/watch?v=dam0GPOAvVI



