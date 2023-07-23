from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
postgres_string = 'postgresql://doadmin:AVNS_B3PZmgQl943DmavUsNZ@db-postgresql-s14a-do-user-14294326-0.b.db.ondigitalocean.com:25060/s14a?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_string
db.init_app(app)

# Here's the code to test the connection:
with app.app_context():
    try:
        with db.engine.connect():
            print("Database connection successful!")
    except Exception as e:
        print("Database connection failed!")
        print(str(e))


class Student(db.Model):
    id = db.Column(db.Integer, primary_keys= True, nullable = False)
    username = db.Column(db.String)
    email = db.Column(db.String)
    phonenumber = db.Column(db.String)
