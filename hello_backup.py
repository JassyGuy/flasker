#from crypt import methods
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user




# Creatre a Flask Instance
app = Flask(__name__)

#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL-PASSWORD'] = 'rmsidrk9!'
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DB'] = 'our_users'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#db = MySQL(app)

#Add Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#New MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rmsidrk9!@localhost/our_users'
#Secret Key !!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know "

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit  = SubmitField("Submit")


#Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#from server import db
#db.create_all()

#Flask Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



#Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
#Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")
            
    return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out! Thanks for Stopping By...")
    return redirect(url_for('login'))

#Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html",
                                   form = form, 
                                   name_to_update = name_to_update)
        except:
            db.session.commit()
            flash("Error! Looks like there was a problem... try again")
            return render_template("dashboard.html",
                                   form = form, 
                                   name_to_update = name_to_update)
    else:
        return render_template("dashboard.html",
                               form = form, 
                               name_to_update = name_to_update,
                               id = id)
        
    return render_template('dashboard.html')

#class Posts(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(255))
#    content = db.Column(Text)
#    author = db.Column(db.String(255))
#    date_posted = db.Column(db.DateTime, default=)
#    slug = db.Column(db.String(255))
    
#Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Do some password stuff!
    password_hash = db.Column(db.String(128))
                              
    @property
    def password(self):
        raise AttributeError('passowrd is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
        
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully !!!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", 
                           form=form, 
                           name=name,
                           our_users=our_users)        
    except:
        flash("Whoops! There was a problem deleting User...Try Again!!")
        return render_template("add_user.html", form=form, 
                           name=name,
                           our_users=our_users)        
    
# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("What's your email", validators=[DataRequired()])
    password_hash = PasswordField("What's your password", validators=[DataRequired()])
    submit = SubmitField("Submit")
            
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
#Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        
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
                               name_to_update = name_to_update,
                               id = id)
            
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
 #   cur = db.connection.cursor()
    
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None: 
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully!")

    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
                           form=form, 
                           name=name,
                           our_users=our_users)
    
# Create a route decorator
@app.route('/')
def index():
    first_name = "Benny"
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

#Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''
        
        pw_to_check = Users.query.filter_by(email=email).first()
        #flash("Form submitted Successfully")
        
        #Check Hasehd Password
        passed = check_password_hash(pw_to_check.password_hash, password)
        
    return render_template("test_pw.html",
        email = email,
        password = password,
        pw_to_check = pw_to_check,
        passed = passed,
        form = form)
    
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

#app.run(port=5001, debug=True)