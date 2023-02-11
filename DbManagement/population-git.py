import random
import string
import psycopg2
import re
import bcrypt

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

with open("./text_documents/companies_short.txt", "r") as companies_f:
    companies = companies_f.read().split('\n')

max_comp_id = len(companies)

regex = re.compile('[^a-zA-Z]')
regex_pass = re.compile('[^a-zA-Z ]')

records = []
for company in companies:
    print(company)

    mail = regex.sub('', company)
    mail = mail + "@gmail.com"

    password = regex_pass.sub('', company).split(' ', 1)[0]
    if len(password) < 5:
        password = ''.join(random.choice(string.printable) for i in range(10))

    # salt = os.urandom(16)
    # plaintext = password.encode()
    # digest = hashlib.pbkdf2_hmac('sha256', salt, plaintext, 1000)

    # digest_hex = digest.hex()

    password_hash = get_hashed_password(password.encode())
    #print(password)

    is_admin = 0
    record = [company, mail, password_hash, is_admin]
    records.append(record)

with open("./text_documents/resources.txt", "r") as resources_f:
    resources = resources_f.read().split('\n')
    resources.pop(-1)

conn = psycopg2.connect(database="postgres",
                        host="greenstock_postgres_1",
                        user="postgres",
                        password="dbAdmin",
                        port="5432")

cursor = conn.cursor()

try:
    cursor.execute("""
        create table companies (
            company_id serial primary key,
            company_name varchar(63) unique not null,
            company_mail varchar(255) unique not null,
            password_hash varchar(255) unique not null,
            is_admin int4
        );
    """)
    #password_salt varchar(63) unique not null,

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

    cursor.execute("""
        create table company_resources (
            company_resource_id serial primary key,
            company_id int4 references companies(company_id),
            resource_id int4 references resources(resource_id),
            stock_amount float not null
        );    
    """)
except:
    print("failed to create one or many tables")

for record in records:
    print(record)
    cursor.execute("""
       insert into companies (company_name, company_mail, password_hash, is_admin)
       values (%s, %s, %s, %s);
    """,
                   (record[0], record[1], record[2], record[3]))

# Populate resources table
for resource in resources:
    pass
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
    cursor.execute("""insert into transactions (buyer_id, seller_id, resource_id, quantity, price_per_ton)
                   values (%s, %s, %s, %s, %s);""", (buyer_id, seller_id, resource_id, quantity, price_per_ton))

for i in range(1, 100):
    buyer_id = round(random.randint(1, max_comp_id), 2)
    resource_id = random.randint(1, max_resource_id)
    quantity = round(random.uniform(5, 1000), 2)
    price_per_ton = round(random.uniform(20, 100), 2)

    cursor.execute("""insert into buy_offers (buyer_id, resource_id, quantity, price_per_ton)
                   values (%s, %s, %s, %s);""", (buyer_id, resource_id, quantity, price_per_ton))


for i in range(1, 100):
    seller_id = round(random.randint(1, max_comp_id), 2)
    resource_id = random.randint(1, max_resource_id)
    quantity = round(random.uniform(5, 1000), 2)
    price_per_ton = round(random.uniform(20, 100), 2)

    cursor.execute("""insert into sell_offers (seller_id, resource_id, quantity, price_per_ton)
                   values (%s, %s, %s, %s);""", (seller_id, resource_id, quantity, price_per_ton))
conn.commit()
cursor.close()
conn.close()
