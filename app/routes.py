from flask import render_template, flash, redirect, url_for, request, session, jsonify
from app import app
from app.forms import LoginForm
from .models import User

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        if (not User(username).verify_password(password)):
            print('invalid login')
        else:
            session['username'] = username
            #flash('Login requested for user {}'.format(form.username.data))
            return redirect(url_for('home'))

    return render_template('login.html',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['retypePassword']
        if (not User(username).register(password, repassword)):
            flash('A user with this username already exists.')
        else:
            session['username'] = username
            flash('Logged in')
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')

@app.route('/home')
def home():
    questions = User(session['username']).get_questions()
    # questions = ['why']
    return render_template('home.html', posts=questions)

@app.route('/interest')
def interest():
    return render_template('interest.html')

@app.route('/otherprofile')
def otherprofile():
    return render_template('otherprofile.html')

@app.route('/searchpage')
def searchpage():
    return render_template('searchpage.html')

@app.route('/profilepage')
def profilepage():
    return render_template('profilepage.html')

@app.route('/add_question', methods=['POST'])
def add_question():
    question = request.form['question']
    tags = request.form['tags']

    if not question:
        flash('You have not entered a question.')
    elif not tags:
        flash('You must give your post at least one tag.')
    else:
        User(session['username']).ask(question, tags)

    return redirect(url_for('home'))


@app.route('/question', methods=['GET'])
def question():
    questiontitle = request.args.get('title')
    #question_answers = get_answers(questiontitle)
    #return render_template('question.html', question_answers=question_answers)
    return render_template('question.html', title=questiontitle)

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    app.logger.debug(search)
    NAMES = []
    searchResult = getUsersStartingWith('sa')
    for user in searchResult:
        NAMES.append(user['username'])
    print(NAMES)
    return jsonify(json_list=NAMES)
@app.route('/updateBio', methods=['POST'])
def updateBio():
    if request.method == 'POST':
        bio = request.form['txtFieldBio']
        print(bio)
        User(session['username']).editBio(bio)
        return redirect(url_for('profilepage'))

