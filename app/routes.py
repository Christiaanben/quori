from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html',form=form)
	
@app.route('/register', methods=['GET','POST'])
def register():
	return render_template('register.html')

@app.route('/home')
def home():
	return render_template('home.html')