from flask import render_template, flash, redirect, url_for, request, session, jsonify
from app import app
from app.forms import LoginForm
from .models import User, getUsersStartingWith, get_interests_titles, add_q_tag
import os


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        if not (User(username)).find():
            error = "Username was not found."
        elif not User(username).verify_password(password):
            error = "Password is incorrect."
        else:
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('login.html', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['retypePassword']
        if not User(username).register(password, repassword):
            error = 'A user with this username already exists.'
        else:
            session['username'] = username
            return redirect(url_for('interest'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    questions = User(session['username']).get_questions()
    interests = get_interests_titles()
    return render_template('home.html', posts=questions, interests=interests)


@app.route('/interest')
def interest():
    interests = get_interests_titles()
    return render_template('interest.html', interests=interests)


@app.route('/add_interests', methods=['POST'])
def add_interests():
    interests = get_interests_titles()
    list_of_interests = interests.data()
    for value in list_of_interests:
        if request.form.get(value['tag']):
            User(session['username']).addInterest(value['tag'])
    return redirect(url_for('home'))


@app.route('/otherprofile')
def otherprofile():
    return render_template('otherprofile.html')


@app.route('/searchpage')
def searchpage():
    return render_template('searchpage.html')


@app.route('/profilepage')
def profilepage():
    user = User(session['username']);
    return render_template('profilepage.html', user=user)


@app.route('/add_question', methods=['POST'])
def add_question():
    title = request.form['title']
    question = request.form['question']
    q_tags = request.form.getlist('Qtags')
    if not title:
        flash('You have not entered a title.')
    elif not question:
        flash('You have not entered a question.')
    elif not q_tags:
        flash('You must give your post at least one tag.')
    else:
        User(session['username']).ask(title, question)
        for tag in q_tags:
            add_q_tag(title, tag)

    return redirect(url_for('home'))


@app.route('/question', methods=['GET'])
def question():
    questiontitle = request.args.get('title')
    # question_answers = get_answers(questiontitle)
    # return render_template('question.html', question_answers=question_answers)
    return render_template('question.html', title=questiontitle)


@app.route('/updateBio', methods=['POST'])
def updateBio():
    if request.method == 'POST':
        bio = request.form['txtFieldBio']
        User(session['username']).editBio(bio)
        return redirect(url_for('profilepage'))


@app.route('/updatePassword', methods=['POST'])
def updatePassword():
    if request.method == 'POST':
        oldPassword = request.form['passwordOld']
        newPassword = request.form['passwordNew']
        retypePassword = request.form['passwordRetype']
        User(session['username']).editPassword(oldPassword, newPassword, retypePassword)
        return redirect(url_for('profilepage'))


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['pic']
        # verander net hierdie na julle profile picture path
        filepath = os.path.join('/home/comango/Desktop/Github Repos/Quori/app/static/profilepictures', f.filename)
        if os.path.isfile(filepath):
            os.remove(filepath)

        f.save(filepath)
        User(session['username']).updateProfilePic(f.filename)
        session['profilepic']=f.filename
        return redirect(url_for('profilepage'))


@app.route('/search/<prefix>')
def search(prefix):
    print(prefix)
    searchResult = getUsersStartingWith(prefix)
    names = ['Basic', 'Ben']
    for user in searchResult:
        names.append(user['username'])
    print(names)
    return jsonify({'suggestions': names})


