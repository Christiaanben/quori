from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

# url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
# username = os.environ.get('neo4j')
# password = os.environ.get('password')

# connects to db when db authetication is off
graph = Graph("http://localhost:7474/db/data/", user='neo4j', password='1234')


# graph = Graph(url + '/db/data/', username=username, password=password)
# graph = Graph('http://localhost:7474', username = 'neo4j', password = 'password')


class User:
    def __init__(self, username):
        self.username = username

    def getSelf(self):
        u = graph.find_one('User', 'username', self.username)
        return u

    def addFollows(self, username):
        query = '''MATCH (a:User),(b:User)
        WHERE a.username = \' ''' + self.username + '''\' AND b.username = \'''' + username + '''\'
		CREATE (a)-[r:Follows]->(b)'''
        graph.run(query)
        # MATCH (a:User),(b:User)

    # WHERE a.username = 'Ricky' AND b.username = 'Maan'
    # CREATE (a)-[r:Follows]->(b)

    def addUpvoted(self, id):
        query = 'MATCH (a:User), (b:Answer) WHERE a.username = \''
        self.username + '\' AND b.id = \' ' + \
        id + '\' CREATE (a)-[r:Upvoted]->(b)'
        graph.run(query)
        # MATCH (a:User),(b:User)

    # WHERE a.username = 'Ricky' AND b.id = 'A2'
    # CREATE (a)-[r:Upvoted]->(b)

    def addPP(self):
        query = 'MATCH (a:User) WHERE a.username = \''
        + self.username + '\' SET a.pp = a.username + \'.jpg\''
        graph.run(query)

    # MATCH (a:User)
    # WHERE a.username = 'Maan'
    # SET a.pp = a.username

    def removeFollows(self, username):
        query = 'MATCH (a:User)-[r:Follows]-(b:User) WHERE a.username = \''
        +self.username + '\' AND b.username = \'' + username + '\' DELETE r'
        graph.run(query)

    # MATCH (a:User)-[r:Follows]-(b:User)
    # WHERE a.username = 'Maan' AND b.username = 'Patrick'
    # DELETE r

    def removeUpvoted(self, id):
        query = 'MATCH (a:User)-[r:Upvoted]-(b:Answer) WHERE a.username = \''
        + self.username + '\' AND b.id = \'' + id + '\'DELETE r '
        graph.run(query)

    # MATCH (a:User)-[r:Upvoted]-(b:Answer)
    # WHERE a.username = 'Maan' AND b.id = 'A5'
    # DELETE r

    def removePP(self):
        query = 'MATCH (a:User) WHERE a.username = \''
        + self.username + '\' SET a.pp = \'temp.jpg\''
        graph.run(query)
        # MATCH (a:User)
        # WHERE a.username = 'Maan'
        # SET a.pp = 'temp.jpg'
        return 0

    def getBio(self):
        query = 'MATCH (a:User) WHERE a.username = {username} RETURN a.bio'
        result = graph.run(query, username=self.username)
        try:
            bio = result.next()
            return bio
        except StopIteration:
            return 'No bio...'

    def editBio(self, bio):
        query = 'MATCH (a:User) WHERE a.username = {username} SET a.bio = {bio}'
        graph.run(query, username=self.username, bio=bio)
        # MATCH (a:User)
        # WHERE a.username = 'Maan'
        # SET a.bio = 'My new bio!'

    def editPassword(self, passwordOld, passwordNew, passwordRetype):
        if (self.verify_password(passwordOld)):
            if (passwordNew != passwordRetype):
                return False
            query = 'MATCH (a:User) WHERE a.username = {username} SET a.password = {passwordNew}'
            graph.run(query, username=self.username,
                      passwordNew=bcrypt.encrypt(passwordNew))
            return True
        # MATCH (a:User)
        # WHERE a.username = 'Maan'
        # SET a.password = 'badPassword42'
        else:
            return False

    def updateProfilePic(self, filename):
        query = 'MATCH (a:User) WHERE a.username = {username} SET a.pp = {pp}'
        graph.run(query, username=self.username, pp=filename)

    def find(self):
        user = graph.find_one('User', 'username', self.username)
        return user

    def register(self, password, repassword):
        if (len(password) < 8):
            return False
        if (len(password) != len(repassword)):
            return False
        if (password != repassword):
            return False
        if not self.find():
            user = Node('User', username=self.username, password=bcrypt.encrypt(
                password), bio="I have questions:)!", pp='temp.jpg')
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def ask(self, title, question):
        user = self.find()
        question = Node(
            "Question",
            id=str(uuid.uuid4()),
            title=title,
            description=question,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, 'Asked', question)
        graph.create(rel)

    def submit_answer(self, answer, question):
        query = '''
			MATCH (question:Question{title:"''' + question + '''"}) MATCH(user:User {username:"''' + self.username + '''"})  MERGE(question)<-[:AnswerTo]-(answer:Answer{id:'A9',title: "''' + answer + '''", timestamp:"1",date:"1", user:"''' + self.username + '''"})<-[:Answered]-(user)
		'''
        graph.run(query)

    def get_questions(self):
        query = '''
            MATCH (user:User)-[:Asked]->(question:Question)
            WHERE user.username = {username}
            RETURN question ORDER BY question.timestamp DESC
            LIMIT 10
            UNION
            MATCH (user:User)-[:Follows]->(:Tag)-[:Tagged]->(question:Question)
            WHERE user.username = {username}
            RETURN question ORDER BY question.timestamp DESC
            LIMIT 10
            UNION  
            MATCH (user:User)-[:Follows]->(p:User)-[:Asked]->(question:Question)
            WHERE user.username = {username}
            RETURN question ORDER BY question.timestamp DESC
            LIMIT 10
        '''
        return graph.run(query, username=self.username)

    def addInterest(self, interest):
        user = self.find()
        tag = graph.find_one('Tag', 'title', interest)
        rel = Relationship(user, 'Follows', tag)
        graph.create(rel)

    def getPP(self):
        query = 'MATCH (a:User) WHERE a.username = {username} RETURN a.pp AS p'
        return graph.run(query, username=self.username).next()

    def getUsername(self):
        query = 'MATCH (a:User) WHERE a.username = {username} RETURN a.username AS un'
        return graph.run(query, username=self.username).next()

    def getSuggestions(self):
        query = '''
        MATCH (myself:User)-[:Follows]->(following:User),
        (following)-[:Follows]->(notFollowing:User),
        (:User)-[up:Upvoted]-(:Answer)-[:Answered]-(notFollowing)
        WHERE myself.username={username} AND NOT (myself)-[:Follows]->(notFollowing)
        RETURN notFollowing, COUNT(up)
        ORDER BY COUNT(up) DESC
        LIMIT 5
        '''
        return graph.run(query, username=self.username)
    
    def addBookmark(self, questionTitle):
        user = self.find()
        question = find_one(questionTitle)
        rel = Relationship(user,'Bookmarked', question)
        graph.create(rel)
    
    def getBookmarkedQuestion(self):
        query = "MATCH (u:User)-[:Bookmarked]->(question:Question) WHERE u.username={username} return question"
        return graph.run(query, username = self.username)

def get_interests_titles():
    query = '''
        MATCH (tag:Tag) RETURN tag.title AS tag
        '''
    return graph.run(query)


def add_q_tag(question_title, interest):
    question = graph.find_one('Question', 'title', question_title)
    tag = graph.find_one('Tag', 'title', interest)
    rel = Relationship(tag, 'Tagged', question)
    graph.create(rel)


def get_similar_users(self):
    # Find three users who are most similar to the logged-in user
    # based on tags they've both blogged about.
    query = '''
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        '''

    return graph.run(query, username=self.username)


def get_commonality_of_user(self, other):
    # Find how many of the logged-in user's posts the other user
    # has liked and which tags they've both blogged about.
    query = '''
        MATCH (they:User {username: {they} })
        MATCH (you:User {username: {you} })
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN SIZE((they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you)) AS likes,
               COLLECT(DISTINCT tag.name) AS tags
        '''

    return graph.run(query, they=other.username, you=self.username).next


def get_todays_recent_posts():
    query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''

    return graph.run(query, today=date())


def find_one(questiontitle):
    return graph.find_one("Question", "title", questiontitle)


def get_answers(questiontitle):
    query = '''
    MATCH (question:Question)<-[:AnswerTo]-(answer:Answer)<-[:Answered]-(u:User) WHERE question.title = {questiontitle} RETURN answer.title AS title, u.username as user, u.pp as pp
    '''
    return graph.run(query, questiontitle=questiontitle)


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


def date():
    return datetime.now().strftime('%Y-%m-%d')


def getUsersStartingWith(prefix):
    query = '''
    MATCH (u:User)
    WHERE LOWER(u.username) STARTS WITH LOWER({prefix})
    RETURN u
    '''
    return graph.run(query, prefix=prefix)

