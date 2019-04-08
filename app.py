# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 05:16:51 2019

@author: ohmkk
"""

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
'''from flask.ext.jsonpify import jsonify'''
from flask import jsonify

db_connect = create_engine('sqlite:///api.db')
app = Flask(__name__)
api = Api(app)

class Spending(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from spending") # This line performs query and returns json result
        #query2 = conn.execute("select sum(amount) from spending")
        result = {'spends': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        '''return {'spending': [i[0] for i in query.cursor.fetchall()]}''' # Fetches first column that is Employee ID
        return jsonify(result)
class Receiving(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from receiving;")
        result = {'receives': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

'''
class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
   ''' 
#@app.route('/add', methods=['POST'])
class AddSpending(Resource):
    def add_spending(self):
        try:
            _json = request.json
            _date = _json['date']
            _reason = _json['reason']
            _amount = _json['amount']
            # validate the received values
            if _date and _reason and _amount and request.method == 'POST':
                #do not save password as a plain text
                #_hashed_password = generate_password_hash(_password)
                # save edits
                sql = "INSERT INTO spending(date, reason, amount) VALUES(%s, %s, %d)"
                data = (_date, _reason, _amount)
                #conn = mysql.connect()
                conn = db_connect.connect()
                cursor = db_connect.cursor()
                conn.cursor()
                conn.execute(sql, data)
                conn.commit()
                #resp = jsonify('Spending added successfully!')
                #resp.status_code = 200
                return
            else:
                return 404
        except Exception as e:
            print(e)
        finally:
            cursor.close()        
            conn.close()
            
class AddReceiving(Resource):
    def add_receiving(self):
        try:
            _json = request.json
            _date = _json['date']
            _from_reason = _json['_from_reason']
            _amount = _json['amount']
            # validate the received values
            if _date and _from_reason and _amount and request.method == 'POST':
                #do not save password as a plain text
                #_hashed_password = generate_password_hash(_password)
                # save edits
                sql = "INSERT INTO receiving(date, from_reason, amount) VALUES(date(%s), %s, %d)"
                data = (_date, _from_reason, _amount)
                #conn = mysql.connect()
                conn = db_connect.connect()
                cursor = db_connect.cursor()
                conn.cursor()
                conn.execute(sql, data)
                conn.commit()
                resp = jsonify('Receiving added successfully!')
                resp.status_code = 200
                return resp
            else:
                return 404
        except Exception as e:
            print(e)
        finally:
            cursor.close()        
            conn.close()
                

api.add_resource(Spending, '/spending',methods=['GET']) # Route_1
api.add_resource(Receiving, '/receiving',methods=['GET']) # Route_2
api.add_resource(AddSpending, '/spending_up',methods=['POST']) # Route_2
api.add_resource(AddReceiving, '/receiving_up',methods=['POST']) # Route_2

'''api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3'''


if __name__ == '__main__':
     app.run(debug = True)