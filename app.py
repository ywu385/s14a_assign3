from flask import Flask, request, render_template, redirect
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://doadmin:password@db-postgresql-s14a-do-user-14294326-0.b.db.ondigitalocean.com:25060/s14a'
db.init_app(app)
# # db = sqlalchemy(app)

# engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except Exception as e:
#     print("Connection failed!")
#     print(str(e))


links = [
    {"label": "Home", "url": "/home"},
    {"label": "About", "url": "/about"},
    {"label": "Users", "url": "/Users"},
    {'label':'Register', 'url':'/register'}
]

app.debug = True

@app.route("/")
def index():
    # return 'Hello, World!'
    return render_template('index.html',navigation=links, header='Home')
    # return render_template('test.html')


@app.route("/home")
def home():
    return render_template('index.html',navigation = links, header='Home')

@app.route("/about")
def about():
    return render_template('about.html',navigation = links, header='About')

@app.route("/Users")
def list():
    with open('data/comment_table.json','r') as f:
        data = json.load(f)
    return render_template('table.html',data = data, header = 'Who has been here?')

@app.route('/success')
def success():
    return render_template('success.html',header='Success!')

@app.route("/register", methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        comments = request.form.get('phone_number')

        data = {'email':email,
                'phone_number':phone_number}
        
     # Append into database here
        return redirect('/success')
    
    return render_template('Form.html', header='Register')

@app.route("/registration", methods = ['GET','POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        data = {'email': email,
                'password': password}
     
         # Adding data into JSON file
        with open('data/registration.json', 'a+') as f:
            f.seek(0)
            try:
                old_data = json.load(f)
            except ValueError:
                old_data = []

            old_data.append(data)

        with open('data/registration.json','w') as f:
            json.dump(old_data,f)

        return redirect('/home')
    return render_template('registration.html', header='Registration')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
