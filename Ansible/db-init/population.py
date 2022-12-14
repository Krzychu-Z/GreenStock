import os
import random
import string
import psycopg2
import re
import hashlib


def random_timestamp(start_year=2017, stop_year=2022, start_month=1, end_month=12):
    year = str(random.randint(start_year, stop_year))
    month = str(random.randint(start_month, end_month))
    day = str(random.randint(1, 28))
    hour = str(random.randint(0, 23))
    minute = str(random.randint(0, 59))
    sec = str(random.randint(0, 59))

    timestamp = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + sec + '.' + '0'
    return timestamp


def random_timestamps(month_diff=1, day_diff=0):
    first_date = random_timestamp()
    month = int(first_date.split('-')[1])

    first_date_2 = first_date.replace(" ", '-')
    day = int(first_date_2.split('-')[2])
    year = int(first_date.split('-')[0])

    month = month + month_diff
    day = day + day_diff

    if day > 28:
        month = month + 1
        day = day - 28

    if month > 12:
        year = year + 1
        month = month - 12

    second_date = str(year) + '-' + str(month) + '-' + str(day) + ' 23:59:59.999999'
    return first_date, second_date


with open("./text_documents/companies.txt", "r") as companies_f:
    companies = companies_f.read().split('\n')

max_comp_id = len(companies)

regex = re.compile('[^a-zA-Z]')
regex_pass = re.compile('[^a-zA-Z ]')

records = []
for company in companies:
    mail = regex.sub('', company)
    mail = mail + "@gmail.com"

    password = regex_pass.sub('', company).split(' ', 1)[0]
    if len(password) < 5:
        password = ''.join(random.choice(string.printable) for i in range(10))

    salt = os.urandom(16)
    plaintext = password.encode()
    digest = hashlib.pbkdf2_hmac('sha256', salt, plaintext, 1000)

    digest_hex = digest.hex()
    record = [company, mail, salt.hex(), digest.hex()]
    records.append(record)

with open("./text_documents/resources.txt", "r") as resources_f:
    resources = resources_f.read().split('\n')
    resources.pop(-1)

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

cursor = conn.cursor()

try:
    cursor.execute("""
        create table companies (
            company_id serial primary key,
            company_name varchar(63) unique not null,
            company_mail varchar(255) unique not null,
            password_salt varchar(63) unique not null,
            password_hash varchar(64) unique not null
        );
    """)

    cursor.execute("""
        create table resources (
            resource_id serial primary key, 
            resource_name varchar(63) unique not null
        );
    """)

    cursor.execute("""
        create table transactions (
            transaction_id serial primary key,
            buyer_id int4 references companies(company_id),
            seller_id int4 references companies(company_id),
            resource_id int4 references resources(resource_id),
            quantity float not null,
            price_per_ton float not null,
            transaction_time timestamp default now()
        );       
    """)

    cursor.execute("""
            create table sell_offers (
                sell_offer_id serial primary key,
                seller_id int4 references companies(company_id),
                resource_id int4 references resources(resource_id),
                quantity float not null,
                price_per_ton float not null,
                offer_start_date timestamp default now(),
                offer_end_date timestamp,
                min_amount float default 1
            );     
    """)

    cursor.execute("""
        create table buy_offers (
            buy_offer_id serial primary key,
            buyer_id int4 references companies(company_id),
            resource_id int4 references resources(resource_id),
            quantity float not null,
            price_per_ton float not null,
            offer_start_date timestamp default now(),
            offer_end_date timestamp default now(),
            min_amount float default 1
        );    
    """)
except:
    print("failed to create one or many tables")

for record in records:
    cursor.execute("""
       insert into companies (company_name, company_mail, password_salt, password_hash)
       values (%s, %s, %s, %s);
    """,
                   (record[0], record[1], record[2], record[3]))

# Populate resources table
for resource in resources:
    pass
    # print(resources)
    # cursor.execute("insert into resources (resource_name) values (%s);", resource)
    # nie wiem, czemu to nie dziala

cursor.execute("insert into resources (resource_name) values ('CO');")
cursor.execute("insert into resources (resource_name) values ('CO2');")
cursor.execute("insert into resources (resource_name) values ('CH4');")
cursor.execute("insert into resources (resource_name) values ('N2O');")
cursor.execute("insert into resources (resource_name) values ('HFC');")
cursor.execute("insert into resources (resource_name) values ('PFC');")
cursor.execute("insert into resources (resource_name) values ('SF6');")
max_resource_id = 7

for i in range(1, 100):
    buyer_id = round(random.randint(1, max_comp_id), 2)

    while True:
        seller_id = round(random.randint(1, max_comp_id), 2)
        if seller_id != buyer_id:
            break
    resource_id = random.randint(1, max_resource_id)
    quantity = round(random.uniform(5, 1000), 2)
    price_per_ton = round(random.uniform(20, 100), 2)
    cursor.execute("""insert into transactions (buyer_id, seller_id, resource_id, quantity, price_per_ton, transaction_time)
                   values (%s, %s, %s, %s, %s, %s);""",
                   (buyer_id, seller_id, resource_id, quantity, price_per_ton, random_timestamp(2017, 2022)))

for i in range(1, 100):
    buyer_id = round(random.randint(1, max_comp_id), 2)
    resource_id = random.randint(1, max_resource_id)
    quantity = round(random.uniform(5, 1000), 2)
    price_per_ton = round(random.uniform(20, 100), 2)

    first_timestamp, second_timestamp = random_timestamps(random.randint(1, 3))
    cursor.execute("""insert into buy_offers (buyer_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date)
                   values (%s, %s, %s, %s, %s, %s);""",
                   (buyer_id, resource_id, quantity, price_per_ton, first_timestamp, second_timestamp))

for i in range(1, 100):
    seller_id = round(random.randint(1, max_comp_id), 2)
    resource_id = random.randint(1, max_resource_id)
    quantity = round(random.uniform(5, 1000), 2)
    price_per_ton = round(random.uniform(20, 100), 2)

    first_timestamp, second_timestamp = random_timestamps(random.randint(1, 3))
    cursor.execute("""insert into sell_offers (seller_id, resource_id, quantity, price_per_ton, offer_start_date, offer_end_date)
                   values (%s, %s, %s, %s, %s, %s);""", (seller_id, resource_id, quantity, price_per_ton, first_timestamp, second_timestamp))
conn.commit()
cursor.close()
conn.close()
