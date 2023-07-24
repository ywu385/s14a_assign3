from flask import Flask, request, render_template, redirect
import json
from flask_sqlalchemy import SQLAlchemy
# from db_init import User
from sqlalchemy import func

import os

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

db = SQLAlchemy()
app = Flask(__name__)
postgres_string = f'postgresql://{db_username}:{db_password}@db-postgresql-s14a-do-user-14294326-0.b.db.ondigitalocean.com:25060/s14a?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_string
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    updated_at = db.Column(db.DateTime, default = func.now(), onupdate=func.now())
    status = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)
    orders = db.relationship('Order', backref='user', lazy=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    item_name = db.Column(db.String)
    item_count = db.Column(db.Integer)
    total = db.Column(db.Integer)
    user_name = db.Column(db.Integer, db.ForeignKey('users.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
   
links = [
    {"label": "Home", "url": "/home"},
    {"label": "Update Info", "url": "/searchuser"},
    {"label": "Users", "url": "/Users"},
    {'label':'Register', 'url':'/adduser'},
    {'label':'Remove User', 'url':'/deleteuser'}
]

app.debug = True


@app.route('/orders')
def orders():
    user_id = request.args.get('user.id')
    orders = db.session.query(Order).filter(Order.user_name == user_id).all()
    if orders is None:
        orders = []
    return render_template('orders.html', orders=orders, navigation=links,header ="Orders")


@app.route("/")
def index():
    # return 'Hello, World!'
    return render_template('index.html',navigation=links, header='Home')
    # return render_template('test.html')

@app.route("/Users")
def userlist(): 
    with app.app_context():
        userslist = db.session.execute(
            db.select(User).order_by(User.id)).scalars()
        return render_template('table.html',users= userslist,navigation = links, header = 'Users')

@app.route("/adduser", methods = ['GET','POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')  
    
        with app.app_context():
            existing_user = User.query.filter(User.email == email).first()
            if existing_user is not None:
               return "User with this email or phone number already exists!", 400

            user = User(email=email,
               phone_number=phone_number,
               status = 1,
               is_admin=False)
           
            db.session.add(user)
            db.session.commit()

            return redirect('/success')
    
    else:
         
        return render_template('adduser.html', navigation = links, header='Registration', message = 'Please Sign Up')
    
@app.route('/deleteuser', methods=['GET','POST'])
def deleteuser():
    if request.method == 'POST':
        user_id = request.form.get('UserId')

        with app.app_context():
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return redirect('/Users')
            else:
                return 'User not found!', 404
    else:
        return render_template('deleteuser.html', navigation = links, header = 'Delete User')


@app.route("/searchuser", methods=['GET', 'POST'])
def searchuser():
    if request.method == 'POST':
        email = request.form.get('email')

        with app.app_context():
            user = User.query.filter_by(email=email).first()

            if user is None:
                return redirect('/adduser?message=User+Email+not+found%2C+please+sign+up')
            else:
                return redirect('/updateuser/' + str(user.id))

    else:
        return render_template('finduser.html', navigation = links, header='Search User')


@app.route("/updateuser/<int:user_id>", methods = ['GET','POST'])
def updateuser(user_id):
    with app.app_context():
        user = User.query.get(user_id) # query for user

        if request.method == 'POST':
            email = request.form.get('email')
            phone_number = request.form.get('phone_number') 
            is_admin = request.form.get('is_admin')
            if is_admin =='yes':
                is_admin = True
            else:
                is_admin = False 
            
            # Update user's information
            user.phone_number = phone_number
            user.is_admin = is_admin
            
            db.session.add(user)
            db.session.commit()

            return redirect('/Users')
        
        else:
            
            return render_template('updateuser.html', navigation = links, user = user, header='Update User')


@app.route('/success')
def success():
    return render_template('success.html',header='Success!')


@app.route("/home")
def home():
    return render_template('index.html',navigation = links, header='Home')


if __name__ == "__main__":
    app.run(debug=True, port=5002)
