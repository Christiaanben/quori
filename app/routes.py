from flask import render_template, flash, redirect, url_for, request, session, jsonify
from app import app
from app.forms import LoginForm
from .models import find_one
from .models import get_answers, dateFromTimeStamp
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
        # for q in questions:
        #     print(
        #         dateFromTimeStamp(q[0]['timestamp'])
        #     )
        interests = get_interests_titles()
        u = User(session.get('username'))
        suggestions = u.getSuggestions()
        followPosts = User(session['username']).getFollowingAnswers()
        return render_template('home.html', posts=questions, interests=interests,
                               pp=User(session['username']).getPP(), suggestions=suggestions,
                               myFunction=get_bookmarked, followingPosts = followPosts, timeStampToDate=dateFromTimeStamp)
    else:
        return redirect(url_for('login'))


@app.route('/searchpage/', methods=['GET', 'POST'])
def searchpage():
    search = request.form['search']
    users = getUsersStartingWith(search)
    return render_template('searchpage.html', users=users, pp=User(session['username']).getPP())


@app.route('/interest')
def interest():
    currentInterets = User(session['username']).getInterest()
    interests = get_interests_titles()
    return render_template('interest.html',currentInterets=currentInterets, interests=interests)


@app.route('/add_interests', methods=['POST'])
def add_interests():
    interests = get_interests_titles()
    list_of_interests = interests.data()
    for value in list_of_interests:
        if request.form.get(value['tag']):
            User(session['username']).addInterest(value['tag'])
        else:
            User(session['username']).removeInterest(value['tag'])
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    name = request.args.get('name')
    error = request.args.get('error')
    userinfo = User(name)
    results = User(session['username']).checkFollow(name)
    return render_template('profilepage.html', user=userinfo, following=results, pp=User(session['username']).getPP(), error = error)


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
        return redirect(url_for('profile', name=session['username']))


@app.route('/updatePassword', methods=['POST'])
def updatePassword():
    error = None
    if request.method == 'POST':       
        oldPassword = request.form['passwordOld']
        newPassword = request.form['passwordNew']
        retypePassword = request.form['passwordRetype']
        if (User(session['username']).verify_password(oldPassword)):            
            if(User(session['username']).editPassword(oldPassword, newPassword, retypePassword) == False):
                error = "Your new passwords do not match."
        else:
            error = "Changing password was unsuccessful."           
            
    return redirect(url_for('profile', name=session['username'], error = error))


@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        try:
            f = request.files['pic']
            full_path = os.path.realpath(__file__)
            path, filename = os.path.split(full_path)
            filepath = os.path.join(path + '/static/profilepictures', f.filename)
            print(filepath)
            if os.path.isfile(filepath):
                os.remove(filepath)
            f.save(filepath)
            User(session['username']).updateProfilePic(f.filename)
            session['profilepic'] = f.filename
        except:
            print('File not found!')
        return redirect(url_for('profile', name=session['username']))


@app.route('/question', methods=['GET', 'POST'])
def question():
    user = User(session['username']).username
    questiontitle = request.args.get('title')
    question = find_one(questiontitle)
    answers = get_answers(questiontitle, user)
    # question_answers = get_answers(questiontitle)
    # return render_template('question.html', question_answers=question_answers)
    return render_template('question.html', title=questiontitle, htmlquestion=question, htmlanswers=answers,
                           pp=User(session['username']).getPP(),timeStampToDate=dateFromTimeStamp)


@app.route('/submit_answer/<title>', methods=['POST'])
def submit_answer(title):
    global questiontitle
    user = User(session['username'])
    answer = request.form['message']
    me = user.submit_answer(answer, title)
    questiontitle = title
    question = find_one(questiontitle)
    answers = get_answers(questiontitle, user.username)
    # question_answers = get_answers(questiontitle)
    # return render_template('question.html', question_answers=question_answers)
    return redirect(url_for('question',title=questiontitle, htmlquestion=question, htmlanswers=answers,
                           pp=User(session['username']).getPP()))


@app.route('/follow/<name>', methods=['GET', 'POST'])
def follow(name):
    print(name)
    User(session['username']).addFollows(name)
    return redirect(url_for('profile', name=name))

@app.route('/unfollow/<name>', methods=['GET', 'POST'])
def unfollow(name):
    print(name)
    User(session['username']).removeFollows(name)
    return redirect(url_for('profile', name=name))

@app.route('/upvote/<answer>/<title>')
def upvote(answer, title):
    user = User(session['username'])
    user.addUpvoted(answer)
    questiontitle = title
    question = find_one(questiontitle)
    answers = get_answers(questiontitle, user.username)
    return redirect(url_for('question', title=questiontitle, htmlquestion=question, htmlanswers=answers, pp=User(session['username']).getPP()))

@app.route('/removeupvote/<answer>/<title>')
def removeupvote(answer, title):
    user = User(session['username'])
    user.removeUpvoted(answer)
    questiontitle = title
    question = find_one(questiontitle)
    answers = get_answers(questiontitle, user.username)
    return redirect(url_for('question', title=questiontitle, htmlquestion=question, htmlanswers=answers, pp=User(session['username']).getPP()))

@app.route('/add_bookmark', methods = ['GET'])
def add_bookmark():
    if (session.get('username')):
        questiontitle = request.args.get('title')
        User(session['username']).addBookmark(questiontitle)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
   
@app.route('/rem_bookmark', methods = ['GET'])
def rem_bookmark():
    if (session.get('username')):
        questiontitle = request.args.get('title')
        User(session['username']).remBookmark(questiontitle)
        return redirect(url_for('bookmarkPage'))
    else:
        return redirect(url_for('login'))

@app.route('/rem_bookmark_home', methods = ['GET'])
def rem_bookmark_home():
    if (session.get('username')):
        questiontitle = request.args.get('title')
        User(session['username']).remBookmark(questiontitle)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))



@app.route('/bookmarkedQuestions')
def bookmarkedQuestions():
    if (session.get('username')):
        return redirect(url_for('bookmarkPage'))
    else:
        return redirect(url_for('login'))


@app.route('/bookmarkPage', methods=['GET', 'POST'])
def bookmarkPage():
    if request.method == 'POST':
        return redirect(url_for('searchpage', prefix=request.form['search']))
    if (session.get('username')):
        questions = User(session['username']).getBookmarkedQuestion()
        interests = get_interests_titles()
        u = User(session.get('username'))
        suggestions = u.getSuggestions()
        followPosts = User(session['username']).getFollowingAnswers()
        return render_template('bookmark.html', posts=questions, interests=interests,
                               pp=User(session['username']).getPP(), suggestions=suggestions,
                               followingPosts = followPosts, timeStampToDate=dateFromTimeStamp)
    else:
        return redirect(url_for('login'))


# @app.route('/get_bookmarked/<title>')
def get_bookmarked(title):
    if (session.get('username')):
        return User(session['username']).getBookmarked(title)

    else:
        return redirect(url_for('login'))
