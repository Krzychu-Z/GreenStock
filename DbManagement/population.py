from datetime import datetime, timedelta
import random
import string
import uuid
import psycopg2
import re
from werkzeug.security import generate_password_hash
import bcrypt

CREATE_COMPANIES_TABLE = ("""
        create table if not exists companies (
            company_id serial primary key,
            public_id text unique not null, 
            company_name text unique not null,
            account_balance float not null default 0,
            company_mail text unique not null,
            password_hash text unique not null,
            is_admin boolean
        );
    """)

CREATE_RESOURCES_TABLE = ("""
        create table if not exists resources (
            resource_id serial primary key, 
            resource_name text unique not null
        );
    """)

CREATE_TRANSACTIONS_TABLE = ("""
        create table if not exists transactions (
            transaction_id serial primary key,
            buyer_id int4 references companies(company_id) on delete cascade,
            seller_id int4 references companies(company_id) on delete cascade,
            resource_id int4 references resources(resource_id) on delete cascade,
            quantity float not null,
            price_per_ton float not null,
            transaction_time timestamp default now()
        );       
    """)

CREATE_SELL_OFFERS_TABLE = ("""
            create table if not exists sell_offers (
                sell_offer_id serial primary key,
                seller_id int4 references companies(company_id) on delete cascade,
                resource_id int4 references resources(resource_id) on delete cascade,
                quantity float not null,
                price_per_ton float not null,
                offer_start_date timestamp default now(),
                offer_end_date timestamp,
                min_amount float default 1
            );     
    """)
 
CREATE_BUY_OFFERS_TABLE = ("""
        create table if not exists buy_offers (
            buy_offer_id serial primary key,
            buyer_id int4 references companies(company_id) on delete cascade,
            resource_id int4 references resources(resource_id) on delete cascade,
            quantity float not null,
            price_per_ton float not null,
            offer_start_date timestamp default now(),
            offer_end_date timestamp default now(),
            min_amount float default 1
        );    
    """)  

CREATE_COMPANY_RESOURCES_TABLE = ("""
        create table if not exists company_resources (
            company_resource_id serial primary key,
            company_id int4 references companies(company_id),
            resource_id int4 references resources(resource_id),
            stock_amount float not null
        );    
    """)

CREATE_STATISTICS_TABLE = ("""
        create table if not exists price_statistics (
            data_id serial primary key, 
            resource_id int4 references resources(resource_id),
            timestamp timestamp default now(),
            price float
        );
    """)

INSERT_INTO_COMPANIES = ("""
       insert into companies (public_id, company_name, account_balance,company_mail, password_hash, is_admin)
       values (%s, %s, %s, %s, %s, %s) returning company_id;
    """)

INSERT_INTO_RESOURCES = ("""
        insert into resources (resource_name) values (%s) returning resource_id;
    """)

INSERT_INTO_TRANSACTIONS = ("""
        insert into transactions (buyer_id, seller_id, resource_id, quantity, price_per_ton, transaction_time)
        values (%s, %s, %s, %s, %s, %s) returning transaction_id;
    """)

INSERT_INTO_BUY_OFFERS = ("""
        insert into buy_offers (buyer_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date, min_amount)
        values (%s, %s, %s, %s, %s, %s, %s) returning buy_offer_id;
    """)

INSERT_INTO_SELL_OFFERS = ("""
        insert into sell_offers (seller_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date, min_amount)
        values (%s, %s, %s, %s, %s, %s, %s) returning sell_offer_id;
    """)

INSERT_INTO_COMPANY_RESOURCES = ("""
        insert into company_resources (company_id, resource_id, stock_amount)
        values (%s, %s, %s) returning company_resource_id;
    """)

INSERT_INTO_STATISTICS = ( """
        insert into price_statistics (resource_id, price) values (%s, %s) returning data_id;
    """)

connection = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="dbAdmin",
                        port="5432")

with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_COMPANIES_TABLE)
            cursor.execute(CREATE_RESOURCES_TABLE)
            cursor.execute(CREATE_COMPANY_RESOURCES_TABLE)
            cursor.execute(CREATE_SELL_OFFERS_TABLE)
            cursor.execute(CREATE_BUY_OFFERS_TABLE)
            cursor.execute(CREATE_TRANSACTIONS_TABLE)
            cursor.execute(CREATE_STATISTICS_TABLE)

            with open("./text_documents/companies.txt", "r") as companies_f:
                companies = companies_f.read().split('\n')

            max_comp_id = len(companies)

            regex = re.compile('[^a-zA-Z]')
            regex_pass = re.compile('[^a-zA-Z ]')

            records = []
            for company in companies:
                public_id = str(uuid.uuid4())

                mail = regex.sub('', company)
                mail = mail + "@gmail.com"

                password = regex_pass.sub('', company).split(' ', 1)[0]
                if len(password) < 5:
                    password = ''.join(random.choice(string.printable) for i in range(10))
                password_hash = generate_password_hash(password, method='sha256')
                balance = random.random() * 1000000;


                record = [public_id, company, balance, mail, password_hash, False]
                records.append(record)
            
            record = [1, "admin", 0, "admin", generate_password_hash("admin", method='sha256'), True]
            records.append(record)

            for record in records:
                cursor.execute(INSERT_INTO_COMPANIES, (record[0], record[1], record[2], record[3], record[4], record[5]))

            with open("./text_documents/resources.txt", "r") as resources_f:
                resources = resources_f.read().split('\n')
                resources.pop(-1)

            for resource in resources:
                cursor.execute(INSERT_INTO_RESOURCES, (resource, ))
            max_resource_id = 7


            for i in range(1, 10):
                buyer_id = round(random.randint(1, max_comp_id), 2)

                while True:
                    seller_id = round(random.randint(1, max_comp_id), 2)
                    if seller_id != buyer_id:
                        break

                resource_id = random.randint(1, max_resource_id-1)
                quantity = round(random.uniform(5, 1000), 2)
                price_per_ton = round(random.uniform(20, 100), 2)

                dt = datetime.now()
                cursor.execute(INSERT_INTO_TRANSACTIONS, (buyer_id, seller_id, resource_id, quantity, price_per_ton, dt)) 


            for i in range(1, 10):
                buyer_id = round(random.randint(1, max_comp_id), 2)
                resource_id = random.randint(1, max_resource_id-1)
                quantity = round(random.uniform(5, 1000), 2)
                price_per_ton = round(random.uniform(20, 100), 2)
                
                start_date = datetime.now()
                end_date = start_date + timedelta(days=7)
                min_amount = 1

                cursor.execute(INSERT_INTO_BUY_OFFERS, (buyer_id, resource_id, quantity, price_per_ton, start_date, end_date, min_amount))

            for i in range(1, 10):
                seller_id = round(random.randint(1, max_comp_id), 2)
                resource_id = random.randint(1, max_resource_id-1)
                quantity = round(random.uniform(5, 1000), 2)
                price_per_ton = round(random.uniform(20, 100), 2)

                start_date = datetime.now()
                end_date = start_date + timedelta(days=7)
                min_amount = 1

                cursor.execute(INSERT_INTO_SELL_OFFERS, (seller_id, resource_id, quantity, price_per_ton, start_date, end_date, min_amount))

            for i in range(1, 10):
                company_id = round(random.randint(1, max_comp_id), 2)
                resource_id = random.randint(1, max_resource_id-1)
                stock_amount = round(random.uniform(5, 1000), 2)

                cursor.execute(INSERT_INTO_COMPANY_RESOURCES, (company_id, resource_id, stock_amount))

connection.commit()
cursor.close()
connection.close()
