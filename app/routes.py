from flask import render_template
from app import app

@app.route('/')
@app.route('/login')
def login():
	user = {'username': 'Dr Brink'}
	return render_template('login.html')
	
@app.route('/register')
def register():
	return render_template('register.html')
