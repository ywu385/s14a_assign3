from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    status = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def main():
    app = Flask(__name__)
    postgres_string = 'postgresql://doadmin:AVNS_B3PZmgQl943DmavUsNZ@db-postgresql-s14a-do-user-14294326-0.b.db.ondigitalocean.com:25060/s14a?sslmode=require'
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_string
    db.init_app(app)



    with app.app_context():
        try:
            with db.engine.connect():
                print("Database connection successful!")
        except Exception as e:
            print("Database connection failed!")
            print(str(e))

    with app.app_context():
        
        db.create_all()

        users = db.session.execute(
            db.select(User).order_by(User.id)).scalars()
        for u in users:
            print(u.as_dict()
                )

        user1 = User(
            phone_number = '1234567890',
            email = 'email@example.com'
        )
        db.session.add(user1)
        db.session.commit()

        userlist = db.session.execute(
            db.select(User).order_by(User.id)).scalars()
        for u in userlist:
            print(u.as_dict()
                )

        # user = db.get_or_404(User, id)
        # print(user.as_dict())