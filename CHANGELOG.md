# 13/02/2023

## DbManagement/app.py (Connect to postgres via localhost)
```
1.   import bcrypt
    from flask import Flask, jsonify, request, make_response
    import jwt
    import datetime
    from functools import wraps
    from flask_sqlalchemy import SQLAlchemy
    import os, hashlib
    import psycopg2
    import uuid
->   from flask_cors import CORS
    from functools import wraps

->    DB_HOST = "localhost"
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "postgres"

    app = Flask(__name__)
->   CORS(app)

    @app.route('/company', methods=['GET'])
    def get_all_companies():
        try:
.
.
.
```

## DbManagement/requirements.txt
```
bcrypt==4.0.1
flask==2.2.2
jwt==1.3.1
Flask-SQLAlchemy==3.0.3
psycopg2==2.9.5
Flask-Cors==3.0.10
```

## Add Deployment/cert.crt and Deployment/private.key!! (Or ask repo owner)

## Deployment/greenstock.conf, Deployment/httpd.conf

## .gitignore, docker-compose.yml, Dockerfile.Apache, Dockerfile.DbManagement

## Setup instructions:
```
- install docker
- install docker compose (probably will have to install from independent repository - Google that)
run with: docker compose up --build --force-recreate -d
run in debug mode: docker compose up --build --force-recreate
remove with: docker compose down

Not to confuse docker compose with docker-compose ! The app was debugged using docker compose. Using docker-compose the app may but doesn't necessarily have to work ;) 
```