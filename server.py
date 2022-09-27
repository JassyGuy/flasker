#from crypt import methods
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import pymysql



# Creatre a Flask Instance
app = Flask(__name__)

#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL-PASSWORD'] = 'rmsidrk9!'
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DB'] = 'our_users'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#db = MySQL(app)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rmsidrk9!@localhost/our_users'
#Secret Key !!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know "

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit  = SubmitField("Submit")


#Initialize The Database
db = SQLAlchemy(app)

#from server import db
#db.create_all()


#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
        
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
#Update Database Record
@app.route('/upload/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form = form, 
                                   name_to_update = name_to_update)
        except:
            db.session.commit()
            flash("Error! Looks like there was a problem... try again")
            return render_template("update.html",
                                   form = form, 
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html",
                               form = form, 
                               name_to_update = name_to_update)
            
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
 #   cur = db.connection.cursor()
    
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).fisrt()
        if user is None: 
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")

    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
                           form=form, 
                           name=name,
                           our_users=our_users)
    
@app.route('/')
def index():
    first_name = "John"
    stuff = "This is <strong>bold</strong> text"
    flash("Welcome To Our Website !")
    
    favorite_pizza = ["Pepperoni", "Chesse", "Mushroom", 41]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

#Create Custom Error Pages

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted Successfully")
        
    return render_template("name.html",
        name = name,
        form = form)

app.run(port=5001, debug=True)