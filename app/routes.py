from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		#flash('Login requested for user {}'.format(form.username.data))
		return redirect('/home')
	return render_template('login.html',form=form)
	
@app.route('/register', methods=['GET','POST'])
def register():
	return render_template('register.html')

@app.route('/home')
def home():
	return render_template('home.html')