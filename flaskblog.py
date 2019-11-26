from flask import Flask, render_template, url_for, flash, redirect
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='e363df91fc9ce812af257d2ed5e4d95f'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__= 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20),unique=True, nullable=False)
	email = db.Column(db.String(100),unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(20), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __init__(self, username, email, image_file, password):
		self.username=username
		self.email=email
		self.image_file=image_file
		self.password=password

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	__tablename__= 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title =  db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default='datetime.utcnow')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))

	def __init__(self, title, date_posted):
		self.title=title
		self.date_posted=date_posted

	def __repr__(self):
		return f"User('{self.title}', '{self.date_posted}')"

@app.route("/home")
def home():
	return render_template('home.html', blog_posts = posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
	form = LoginForm()
	return render_template('login.html', title='Login', form=form)
