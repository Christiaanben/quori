from flask import render_template, flash, redirect, url_for, request, session, jsonify
from app import app
from app.forms import LoginForm
from .models import find_one
from .models import get_answers
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
    print(session['username'])
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('username'):
        questions = User(session['username']).get_questions()
        interests = get_interests_titles()
        return render_template('home.html', posts=questions, interests=interests, pp=User(session['username']).getPP())
    else:
        return redirect(url_for('login'))


@app.route('/searchpage/', methods=['GET', 'POST'])
def searchpage():
    search = request.form['search']
    users = getUsersStartingWith(search)
    return render_template('searchpage.html', users=users, pp=User(session['username']).getPP())
    return


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


@app.route('/follow/<name>', methods=['GET', 'POST'])
def follow(name):
    User(session['username']).addFollows(name)

@app.route('/otherprofile/<name>', methods=['GET', 'POST'])
def otherprofile(name):
    userinfo = User(name)
    return render_template('profilepage.html', user=userinfo, pp=User(session['username']).getPP())


@app.route('/profilepage', methods=['GET', 'POST'])
def profilepage():
    if request.method == 'POST':
        return redirect(url_for('searchpage', prefix=request.form['search']))
    user = User(session['username'])
    return render_template('profilepage.html', user=user, pp=User(session['username']).getPP())


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
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        print(path + ' --> ' + filename + "\n")
        filepath = os.path.join(path + '/static/profilepictures', f.filename)
        print(filepath)
        if os.path.isfile(filepath):
            os.remove(filepath)

        f.save(filepath)
        User(session['username']).updateProfilePic(f.filename)
        session['profilepic'] = f.filename
        return redirect(url_for('profilepage'))


@app.route('/question', methods=['GET'])
def question():
    questiontitle = request.args.get('title')
    question = find_one(questiontitle)
    answers = get_answers(questiontitle)
    # question_answers = get_answers(questiontitle)
    # return render_template('question.html', question_answers=question_answers)
    return render_template('question.html', title=questiontitle, htmlquestion=question, htmlanswers=answers,
                           pp=User(session['username']).getPP())


@app.route('/submit_answer/<title>', methods=['POST'])
def submit_answer(title):
    global questiontitle
    user = User(session['username'])
    answer = request.form['message']
    me = user.submit_answer(answer, title)
    questiontitle = title
    question = find_one(questiontitle)
    answers = get_answers(questiontitle)
    # question_answers = get_answers(questiontitle)
    # return render_template('question.html', question_answers=question_answers)
    return render_template('question.html', title=questiontitle, htmlquestion=question, htmlanswers=answers)

@app.route('/add_bookmark', methods = ['GET'])
def add_bookmark():
    if (session.get('username')):
        questiontitle = request.args.get('title')
        User(session['username']).addBookmark(questiontitle)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
