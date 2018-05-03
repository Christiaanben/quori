from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		#flash('Login requested for user {}'.format(form.username.data))
		return redirect(url_for('home'))
	return render_template('login.html',form=form)
	
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'POST':
		print("Hello test\n")
		username = request.form['username']
		password = request.form['password']
		if (not User(username).register(password)):
			flash('A user with this username already exists.')
		else:
			session['username'] = username
			flash('Logged in')
			return redirect(url_for('home'))
	return render_template('register.html')

@app.route('/home')
def home():
	return render_template('home.html')
