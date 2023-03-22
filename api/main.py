from flask import Flask, jsonify
from sqlalchemy import create_engine
from datetime import datetime
from flask_restx import Api, Namespace, Resource, \
    reqparse, inputs, fields

# Seting variables to connect to Database
host = "34.175.139.210"
user = "root"
passw = "sN73p647h4VBqeRbDw1d"
database = "hm_sample"
port = "3306"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = "Chloé's REST API with FLASK!",
    description = """
        This RESTS API is an API built with FLASK and FLASK-RESTX libraries.
        """,
    contact = "chloestad@student.ie.edu",
    endpoint = "/api/v1"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    )
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()


# -------------------------- Customers --------------------------
customers = Namespace('customer',
    description = 'All operations related to customers',
    path='/api')
api.add_namespace(customers)

@customers.route("/customer")
class get_all_users(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customer
            LIMIT 10000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/<string:id>")
@customers.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):

    @api.response(404, "CUSTOMER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM customer
            WHERE customer_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# -------------------------- Articles --------------------------
articles = Namespace('articles',
    description = 'All operations related to articles',
    path='/api')
api.add_namespace(articles)

@articles.route("/articles")
class get_all_articles(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM articles
            LIMIT 10000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# -------------------------- Transactions --------------------------
transactions = Namespace('transactions',
    description = 'All operations related to transactions',
    path='/api')
api.add_namespace(transactions)

@transactions.route("/transactions")
class get_all_articles(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions
            LIMIT 10000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug = True, port = 5005)