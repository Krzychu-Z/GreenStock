import bcrypt
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import os, hashlib
import psycopg2
import uuid
from functools import wraps

DB_HOST = "postgres"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "postgres"

app = Flask(__name__)


@app.route('/company', methods=['GET'])
def get_all_companies():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        cursor.execute("""
        select * from companies;
        """)

        output = []
        companies = cursor.fetchall()
        for company in companies:
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            company_data = {}
            company_data['company_id'] = company[0]
            company_data['company_name'] = company[1]
            company_data['company_mail'] = company[2]
            company_data['hassword_hash'] = company[3]
            company_data['is_admin'] = company[4]
            company_data['date'] = dt
            company_data['timestamp'] = ts
            output.append(company_data)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
        return jsonify({'error': "Error occured while fetching data from database"})

    finally:
        if conn:
            cursor.close()
            conn.close()
            return jsonify({'users': output})


@app.route('/company/<company_id>', methods=['GET'])
def get_one_company(company_id):
    if not company_id.isdigit():
        return jsonify({'error': "The company ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from companies where company_id=%(company_id)s;"
        cursor.execute(select_statement, {'company_id': company_id})

        company = cursor.fetchall()[0]

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        output = []
        company_data = {}
        company_data['company_id'] = company[0]
        company_data['company_name'] = company[1]
        company_data['company_mail'] = company[2]
        company_data['hassword_hash'] = company[3]
        company_data['is_admin'] = company[4]
        company_data['date'] = dt
        company_data['timestamp'] = ts
        output.append(company_data)

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'company': output})
    except:
        return jsonify({'error': "No company with given ID"})


@app.route('/company', methods=['POST'])
def create_company():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        data = request.get_json(force=True)

        password = data['password'].encode()

        result = hashlib.sha256(password)
        password_hash = result.hexdigest()

        cursor.execute("""
        insert into companies (company_name, company_mail, password_hash, is_admin)
        values (%s, %s, %s, %s);
        """,
                       (data['company_name'], data['company_mail'], password_hash, 0))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data into PostgreSQL table", error)
        return jsonify({'error': "Error inserting data into PostgreSQL table"})

    finally:
        # closing the connection
        if conn:
            cursor.close()
            conn.close()
            return jsonify({'message': 'New company created'})


@app.route('/company/promote/<company_id>', methods=['PUT'])
def promote_company(company_id):
    if not company_id.isdigit():
        return jsonify({'error': "The company ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from companies where company_id=%(company_id)s;"
        cursor.execute(select_statement, {'company_id': company_id})
        company = cursor.fetchall()[0]

        update_statement = "update companies set is_admin = 1 where company_id = %(company_id)s;"
        cursor.execute(update_statement, {'company_id': company_id})

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': "Update Successful"})
    except:
        return jsonify({'error': "Error while updating record"})


@app.route('/company/<company_id>', methods=['DELETE'])
def delete_user(company_id):
    if not company_id.isdigit():
        return jsonify({'error': "The company ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from companies where company_id=%(company_id)s;"
        cursor.execute(select_statement, {'company_id': company_id})
        company = cursor.fetchall()[0]

        delete_statement = "delete from companies where company_id = %(company_id)s;"
        cursor.execute(delete_statement, {'company_id': company_id})

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': "Delete Successful"})
    except:
        return jsonify({'error': "Error while deleting record"})


@app.route('/resources', methods=['GET'])
def get_all_resources():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        cursor.execute("""
        select * from resources;
        """)

        output = []
        resources = cursor.fetchall()
        for resource in resources:
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            resource_data = {}
            resource_data['resource_id'] = resource[0]
            resource_data['resource_name'] = resource[1]
            resource_data['date'] = dt
            resource_data['timestamp'] = ts
            output.append(resource_data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'resources': output})

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
        return jsonify({'error': "Error occured while fetching data from database"})


@app.route('/resource/<resource_id>', methods=['GET'])
def get_one_resource(resource_id):
    if not resource_id.isdigit():
        return jsonify({'error': "The resource ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from resources where resource_id=%(resource_id)s;"
        cursor.execute(select_statement, {'resource_id': resource_id})

        resource = cursor.fetchall()[0]

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        output = []
        resource_data = {}
        resource_data['resource_id'] = resource[0]
        resource_data['resource_name'] = resource[1]
        resource_data['date'] = dt
        resource_data['timestamp'] = ts
        output.append(resource_data)

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'resource': output})
    except:
        return jsonify({'error': "No resource with given ID"})


@app.route('/resource', methods=['POST'])
def create_resource():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        data = request.get_json(force=True)
        resource_name = data['resource_name']

        select_statement = "insert into resources (resource_name) values (%(resource_name)s);"
        cursor.execute(select_statement, {'resource_name': resource_name})

        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data into PostgreSQL table", error)
        return jsonify({'error': "Error inserting data into PostgreSQL table"})

    finally:
        # closing the connection
        if conn:
            cursor.close()
            conn.close()
            return jsonify({'message': 'New resource created'})


@app.route('/buy_offers', methods=['GET'])
def get_all_buy_offers():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        cursor.execute("""
        select * from buy_offers;
        """)

        output = []
        offers = cursor.fetchall()
        for offer in offers:
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            offer_data = {}
            offer_data['buy_offer_id'] = offer[0]
            offer_data['buyer_id'] = offer[1]
            offer_data['resource_id'] = offer[2]
            offer_data['quantity'] = offer[3]
            offer_data['price_per_ton'] = offer[4]
            offer_data['offer_start_date'] = offer[5]
            offer_data['offer_end_date'] = offer[6]
            offer_data['min_amount'] = offer[7]
            offer_data['date'] = dt
            offer_data['timestamp'] = ts
            output.append(offer_data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'buy_offers': output})

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
        return jsonify({'error': "Error occured while fetching data from database"})


@app.route('/buy_offers/<buy_offer_id>', methods=['GET'])
def get_one_buy_offer(buy_offer_id):
    if not buy_offer_id.isdigit():
        return jsonify({'error': "The buy offer ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from buy_offers where buy_offer_id=%(buy_offer_id)s;"
        cursor.execute(select_statement, {'buy_offer_id': buy_offer_id})

        offer = cursor.fetchall()[0]

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        offer_data = {}
        offer_data['buy_offer_id'] = offer[0]
        offer_data['buyer_id'] = offer[1]
        offer_data['resource_id'] = offer[2]
        offer_data['quantity'] = offer[3]
        offer_data['price_per_ton'] = offer[4]
        offer_data['offer_start_date'] = offer[5]
        offer_data['offer_end_date'] = offer[6]
        offer_data['min_amount'] = offer[7]
        offer_data['date'] = dt
        offer_data['timestamp'] = ts

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'buy_offer': offer_data})
    except:
        return jsonify({'error': "No buy offers with given ID"})


@app.route('/buy_offer', methods=['POST'])
def create_buy_offer():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        data = request.get_json(force=True)

        buyer_id = data['buyer_id']
        resource_id = data['resource_id']
        quantity = data['quantity']
        price_per_ton = data['price_per_ton']
        offer_start_date = data['offer_start_date']
        offer_end_date = data['offer_end_date']
        min_amount = data['min_amount']

        cursor.execute("""
        insert into buy_offers (buyer_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date, min_amount)
        values (%s, %s, %s, %s, %s, %s, %s);
        """,
                       (buyer_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date, min_amount))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data into PostgreSQL table", error)
        return jsonify({'error': "Error inserting data into PostgreSQL table"})

    finally:
        # closing the connection
        if conn:
            cursor.close()
            conn.close()
            return jsonify({'message': 'New buy offer created'})


@app.route('/buy_offer/<buy_offer_id>', methods=['DELETE'])
def delete_buy_offer(buy_offer_id):
    if not buy_offer_id.isdigit():
        return jsonify({'error': "The buy offer ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from buy_offers where buy_offer_id=%(buy_offer_id)s;"
        cursor.execute(select_statement, {'buy_offer_id': buy_offer_id})
        offer = cursor.fetchall()[0]

        delete_statement = "delete from buy_offers where buy_offer_id = %(buy_offer_id)s;"
        cursor.execute(delete_statement, {'buy_offer_id': buy_offer_id})

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': "Delete Successful"})
    except:
        return jsonify({'error': "Error while deleting record"})


@app.route('/sell_offers', methods=['GET'])
def get_all_sell_offers():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        cursor.execute("""
        select * from sell_offers;
        """)

        output = []
        offers = cursor.fetchall()
        for offer in offers:
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            offer_data = {}
            offer_data['sell_offer_id'] = offer[0]
            offer_data['seller_id'] = offer[1]
            offer_data['resource_id'] = offer[2]
            offer_data['quantity'] = offer[3]
            offer_data['price_per_ton'] = offer[4]
            offer_data['offer_start_date'] = offer[5]
            offer_data['offer_end_date'] = offer[6]
            offer_data['min_amount'] = offer[7]
            offer_data['date'] = dt
            offer_data['timestamp'] = ts
            output.append(offer_data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'sell_offers': output})

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
        return jsonify({'error': "Error occured while fetching data from database"})


@app.route('/sell_offers/<sell_offer_id>', methods=['GET'])
def get_one_sell_offer(sell_offer_id):
    if not sell_offer_id.isdigit():
        return jsonify({'error': "The sell offer ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        # cursor.execute("""
        # select * from companies where company_id=%(company_id)s;
        # """, (company_id)
        # )

        select_statement = "select * from sell_offers where sell_offer_id=%(sell_offer_id)s;"
        cursor.execute(select_statement, {'sell_offer_id': sell_offer_id})

        offer = cursor.fetchall()[0]

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        offer_data = {}
        offer_data['sell_offer_id'] = offer[0]
        offer_data['seller_id'] = offer[1]
        offer_data['resource_id'] = offer[2]
        offer_data['quantity'] = offer[3]
        offer_data['price_per_ton'] = offer[4]
        offer_data['offer_start_date'] = offer[5]
        offer_data['offer_end_date'] = offer[6]
        offer_data['min_amount'] = offer[7]
        offer_data['date'] = dt
        offer_data['timestamp'] = ts

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'sell_offer': offer_data})
    except:
        return jsonify({'error': "No sell offers with given ID"})


@app.route('/sell_offer', methods=['POST'])
def create_sell_offer():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        data = request.get_json(force=True)

        seller_id = data['seller_id']
        resource_id = data['resource_id']
        quantity = data['quantity']
        price_per_ton = data['price_per_ton']
        offer_start_date = data['offer_start_date']
        offer_end_date = data['offer_end_date']
        min_amount = data['min_amount']

        cursor.execute("""
        insert into sell_offers (seller_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date, min_amount)
        values (%s, %s, %s, %s, %s, %s, %s);
        """,
                       (seller_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date, min_amount))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data into PostgreSQL table", error)
        return jsonify({'error': "Error inserting data into PostgreSQL table"})

    finally:
        # closing the connection
        if conn:
            cursor.close()
            conn.close()
            return jsonify({'message': 'New sell offer created'})


@app.route('/sell_offer/<sell_offer_id>', methods=['DELETE'])
def delete_sell_offer(sell_offer_id):
    if not sell_offer_id.isdigit():
        return jsonify({'error': "The sell offer ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from sell_offers where sell_offer_id=%(sell_offer_id)s;"
        cursor.execute(select_statement, {'sell_offer_id': sell_offer_id})
        offer = cursor.fetchall()[0]
        print(offer)

        delete_statement = "delete from sell_offers where sell_offer_id = %(sell_offer_id)s;"
        cursor.execute(delete_statement, {'sell_offer_id': sell_offer_id})

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': "Delete Successful"})
    except:
        return jsonify({'error': "Error while deleting record"})


@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        cursor.execute("""
        select * from transactions;
        """)

        output = []
        transactions = cursor.fetchall()
        for transaction in transactions:
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            transaction_data = {}
            transaction_data['transaction_id'] = transaction[0]
            transaction_data['buyer_id'] = transaction[1]
            transaction_data['seller_id'] = transaction[2]
            transaction_data['resource_id'] = transaction[3]
            transaction_data['quantity'] = transaction[4]
            transaction_data['price_per_ton'] = transaction[5]
            transaction_data['transaction_date'] = transaction[6]
            transaction_data['date'] = dt
            transaction_data['timestamp'] = ts
            output.append(transaction_data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'transactions': output})

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
        return jsonify({'error': "Error occured while fetching data from database"})


@app.route('/transactions/<transaction_id>', methods=['GET'])
def get_one_transaction(transaction_id):
    if not transaction_id.isdigit():
        return jsonify({'error': "The transaction ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from transactions where transaction_id=%(transaction_id)s;"
        cursor.execute(select_statement, {'transaction_id': transaction_id})

        transaction = cursor.fetchall()[0]

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        transaction_data = {}
        transaction_data['transaction_id'] = transaction[0]
        transaction_data['buyer_id'] = transaction[1]
        transaction_data['seller_id'] = transaction[2]
        transaction_data['resource_id'] = transaction[3]
        transaction_data['quantity'] = transaction[4]
        transaction_data['price_per_ton'] = transaction[5]
        transaction_data['transaction_time'] = transaction[6]
        transaction_data['date'] = dt
        transaction_data['timestamp'] = ts

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'transaction': transaction_data})
    except:
        return jsonify({'error': "No transactions with given ID"})


@app.route('/transaction', methods=['POST'])
def create_transaction():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        data = request.get_json(force=True)

        buyer_id = data['buyer_id']
        seller_id = data['seller_id']
        resource_id = data['resource_id']
        quantity = data['quantity']
        price_per_ton = data['price_per_ton']
        transaction_time = data['transaction_time']

        cursor.execute("""
        insert into transactions (buyer_id, seller_id, resource_id, quantity, price_per_ton, transaction_time)
        values (%s, %s, %s, %s, %s, %s);
        """,
                       (buyer_id, seller_id, resource_id, quantity, price_per_ton, transaction_time))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data into PostgreSQL table", error)
        return jsonify({'error': "Error inserting data into PostgreSQL table"})

    finally:
        # closing the connection
        if conn:
            cursor.close()
            conn.close()
            return jsonify({'message': 'New transaction created'})


@app.route('/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    if not transaction_id.isdigit():
        return jsonify({'error': "The transaction ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from transactions where transaction_id=%(transaction_id)s;"
        cursor.execute(select_statement, {'transaction_id': transaction_id})
        transaction = cursor.fetchall()[0]
        print(transaction)

        delete_statement = "delete from transactions where transaction_id = %(transaction_id)s;"
        cursor.execute(delete_statement, {'transaction_id': transaction_id})

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': "Delete Successful"})
    except:
        return jsonify({'error': "Error while deleting record"})


@app.route('/company_resources', methods=['GET'])
def get_all_company_resources():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        cursor.execute("""
        select * from company_resources;
        """)

        output = []
        company_resources = cursor.fetchall()
        for resource in company_resources:
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            resource_data = {}
            resource_data['company_resource_id'] = resource[0]
            resource_data['company_id'] = resource[1]
            resource_data['resource_id'] = resource[2]
            resource_data['stock_amount'] = resource[3]
            resource_data['date'] = dt
            resource_data['timestamp'] = ts
            output.append(resource_data)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'company_resources': output})

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
        return jsonify({'error': "Error occured while fetching data from database"})


@app.route('/company_resources/<company_resource_id>', methods=['GET'])
def get_one_company_resource(company_resource_id):
    if not company_resource_id.isdigit():
        return jsonify({'error': "The company resource ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from company_resources where company_resource_id=%(company_resource_id)s;"
        cursor.execute(select_statement, {'company_resource_id': company_resource_id})

        resource = cursor.fetchall()[0]

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        resource_data = {}
        resource_data['company_resource_id'] = resource[0]
        resource_data['company_id'] = resource[1]
        resource_data['resource_id'] = resource[2]
        resource_data['stock_amount'] = resource[3]
        resource_data['date'] = dt
        resource_data['timestamp'] = ts

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'company_resource': resource_data})
    except:
        return jsonify({'error': "No company resource with given ID"})


@app.route('/company_resources', methods=['POST'])
def create_company_resource():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        data = request.get_json(force=True)

        company_id = data['company_id']
        resource_id = data['resource_id']
        stock_amount = data['stock_amount']

        cursor.execute("""
        insert into company_resources (company_id, resource_id, stock_amount)
        values (%s, %s, %s);
        """,
                       (company_id, resource_id, stock_amount))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data into PostgreSQL table", error)
        return jsonify({'error': "Error inserting data into PostgreSQL table"})

    finally:
        # closing the connection
        if conn:
            cursor.close()
            conn.close()
            return jsonify({'message': 'New company resource created'})


@app.route('/company_resources/<company_resource_id>', methods=['DELETE'])
def delete_company_resource(company_resource_id):
    if not company_resource_id.isdigit():
        return jsonify({'error': "The company resource ID you provided is not a digit"})

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        select_statement = "select * from company_resources where company_resource_id=%(company_resource_id)s;"
        cursor.execute(select_statement, {'company_resource_id': company_resource_id})
        company_resource = cursor.fetchall()[0]

        delete_statement = "delete from company_resources where company_resource_id = %(company_resource_id)s;"
        cursor.execute(delete_statement, {'company_resource_id': company_resource_id})

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': "Delete Successful"})
    except:
        return jsonify({'error': "Error while deleting record"})


@app.route('/login', methods=['POST'])
def login():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor()

    data = request.get_json(force=True)
    company_name = data['company_name']
    password = data['password']

    select_statement = "select * from companies where company_name=%(company_name)s;"
    cursor.execute(select_statement, {'company_name': company_name})
    company = cursor.fetchall()[0]

    if not company:
        return jsonify({'result': 'fail'})

    password_hash = company[3]
    user_pass_hash = hashlib.sha256(password.encode()).hexdigest()

    if password_hash == user_pass_hash:
        # token = jwt.encode({'company_id' : company[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app_key)

        return jsonify({'result': 'success'})
    return jsonify({'result': 'fail'})


if __name__ == '__main__':
    app.run(debug=True)