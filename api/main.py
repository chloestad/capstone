from flask import Flask, jsonify
from sqlalchemy import create_engine
from datetime import datetime
from flask_restx import Api, Namespace, Resource, \
    reqparse, inputs, fields

# Seting variables to connect to Database
host = "34.175.139.210"
user = "root"
passw = "sN73p647h4VBqeRbDw1d"
# database = "hm_sample"
database = "hm"
port = "3306"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = "Chloé's Rest API with FLASK - CAPSTONE",
    description = """
        This RESTS API is an API built with FLASK and FLASK-RESTX libraries to retrieve data from my Google Cloud
        database.
        """,
    contact = "chloestad@student.ie.edu",
    endpoint = "/api"
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


# ------------------------------------------ CUSTOMERS ------------------------------------------
'''
Customers endpoints:
In this part of the code I created the customers endpoints to create 
the visualization of the data in streamlit. I created an endpoint to retrieve all customers
data, but wasn't called to optimize loading time since the table has a lot of entries.
'''

customers = Namespace('Customers',
    description = 'All operations related to customers',
    path='/api')
api.add_namespace(customers)

@customers.route("/customers")
# Endpoint to get all customers table
# This one won't be used to optimize loading time.
class get_all_users(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customers;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/ages")
# Endpoint to get the data from the table customers_by_age.
# This table is a group by of customers by age. It has the 
# number of customers by age.
class get_customer_by_age(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customers_by_age;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/ages/spent")
# Endpoint to get the data from the table total_spent_by_age.
# This table is a group by of customers by age. It has the 
# total amount spent by customers by age. It comes from a merge
# with the transactions table.
class get_amount_spent_age(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM total_spent_by_age;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/<string:id>")
@customers.doc(params = {'id': 'The ID of the user'})
# Endpoint to get the data of a specific customers by customer_id.
class select_user(Resource):

    @api.response(404, "CUSTOMER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM customers
            WHERE customer_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# ------------------------------------------ ARTICLES ------------------------------------------
'''
Articles endpoints:
In this part of the code I created the articles endpoints to create 
the visualization of the data in streamlit. I created an endpoint to retrieve all articles
data, but wasn't called to optimize loading time since the table has a lot of entries.
'''

articles = Namespace('Articles',
    description = 'All operations related to articles',
    path='/api')
api.add_namespace(articles)

@articles.route("/articles")
# Endpoint to get all articles table
# This one won't be used to optimize loading time.
class get_all_articles(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM articles;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@articles.route("/articles/top/product")
# Endpoint to get the data from the table product_count.
# This table is a group by product type name. It has the 
# number of products by product_type_name.
class get_top_articles(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM product_count;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@articles.route("/articles/top/color")
# Endpoint to get the data from the table color_count.
# This table is a group by color. It has the 
# number of products by color.
class get_top_colors(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM color_count;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@articles.route("/articles/sold/count")
# Endpoint to get the data from the table product_name_sales_count.
# This table is a group by color. It has the 
# number of products by color.
class get_top_articles_sold(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM product_name_sales_count;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@articles.route("/articles/sold/revenue")
# Endpoint to get the data from the table product_name_sales_sum.
# This table comes from a merge with transactions. It is a group by
# product name that sums price for each transaction by product.
class get_top_articles_sold_rev(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM product_name_sales_sum;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@articles.route("/articles/<string:id>")
@articles.doc(params = {'id': 'The ID of the article'})
# Endpoint to get the data of a specific article by aticle_id.
class select_user(Resource):

    @api.response(404, "ARTICLE not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM articles
            WHERE article_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# ------------------------------------------ TRANSACTIONS ------------------------------------------
'''
Transactions endpoints:
In this part of the code I created the transactions endpoints to create 
the visualization of the data in streamlit. I created an endpoint to retrieve all transactions
data, but wasn't called to optimize loading time since the table has a lot of entries.
'''

transactions = Namespace('Transactions',
    description = 'All operations related to transactions',
    path='/api')
api.add_namespace(transactions)

@transactions.route("/transactions")
# Endpoint to get all transactions table
# This one won't be used to optimize loading time.
class get_all_transactions(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@transactions.route("/transactions/sum/<string:start_date>/<string:end_date>")
@transactions.doc(params = {'start_date': 'The start date', 'end_date': 'The end date'})
# Endpoint to get the sum of transactions by day (revenue). It comes from a group
# by date and sums price for each day. The endpoint also has two parameters: start_date and 
# end_date to get the data between the start end end date.
class select_transactions_by_date(Resource):

    @api.response(404, "TRANSACTIONS not found")
    def get(self, start_date, end_date):
        conn = connect()
        select = """
            SELECT *
            FROM group_by_price_channel
            WHERE t_dat BETWEEN '{0}' AND '{1}'""".format(start_date, end_date)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@transactions.route("/transactions/avg/<string:start_date>/<string:end_date>")
@transactions.doc(params = {'start_date': 'The start date', 'end_date': 'The end date'})
# Endpoint to get the average of transactions by day (revenue). It comes from a group
# by date and average price for each day. The endpoint also has two parameters: start_date and 
# end_date to get the data between the start end end date.
class select_transactions_by_date(Resource):

    @api.response(404, "TRANSACTIONS not found")
    def get(self, start_date, end_date):
        conn = connect()
        select = """
            SELECT *
            FROM transactions_per_day_avg
            WHERE t_dat BETWEEN '{0}' AND '{1}'""".format(start_date, end_date)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug = True, port = 5005)