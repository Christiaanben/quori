from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

# url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
# username = os.environ.get('neo4j')
# password = os.environ.get('password')

graph = Graph("http://localhost:7474/db/data/", user='neo4j', password='1234')

class User:
    def __init__(self, username):
        self.username = username

    def getSelf(self):
        u = graph.find_one('User', 'username', self.username)
        return u

    def addFollows(self, user):
        query = '''MATCH (a:User),(b:User)
        WHERE a.username = {selfusername} AND b.username = {otheruser} MERGE (a)-[r:Follows]->(b)'''
        graph.run(query, selfusername=self.username, otheruser=user)
        # MATCH (a:User),(b:User)

    def checkFollow(self, user):
        query = '''MATCH (u1:User)-[:Follows]-(u2:User) WHERE u1.username={selfun} AND u2.username={otherusern} Return u1'''
        result = graph.run(query, selfun=self.username, otherusern=user)
        try:
            bio = result.next()
            return 1
        except StopIteration:
            return 0

    def addUpvoted(self, title):
        query = '''
		MATCH (a:User), (b:Answer) WHERE a.username = "''' + self.username + '''" AND b.title =  "''' + title + '''" MERGE (a)-[r:Upvoted]->(b)'''
        graph.run(query)

    def addPP(self):
        query = 'MATCH (a:User) WHERE a.username = \''
        + self.username + '\' SET a.pp = a.username + \'.jpg\''
        graph.run(query)

    def removeFollows(self, username):
        query = 'MATCH (a:User)-[r:Follows]-(b:User) WHERE a.username = \''
        +self.username + '\' AND b.username = \'' + username + '\' DELETE r'
        graph.run(query)

    def removeUpvoted(self, title):
        query = '''
		MATCH (n:User{username: "'''+self.username+'''" })-[r:Upvoted]->(:Answer{title:"'''+title+'''"})
		DELETE r'''
        graph.run(query)

    def removePP(self):
        query = 'MATCH (a:User) WHERE a.username = \''
        + self.username + '\' SET a.pp = \'temp.jpg\''
        graph.run(query)
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

    def editPassword(self, passwordOld, passwordNew, passwordRetype):
        if (self.verify_password(passwordOld)):
            if (passwordNew != passwordRetype):
                return False
            query = 'MATCH (a:User) WHERE a.username = {username} SET a.password = {passwordNew}'
            graph.run(query, username=self.username,
                      passwordNew=bcrypt.encrypt(passwordNew))
            return True
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
        if answer == "":
            return
        query = '''
			MATCH (question:Question{title:"''' + question + '''"}) MATCH(user:User {username:"''' + self.username + '''"})  MERGE(question)<-[:AnswerTo]-(answer:Answer{id:'A9',title: "''' + answer + '''", timestamp:"1",date:"1", user:"''' + self.username + '''"})<-[:Answered]-(user)
		'''
        graph.run(query)

    def get_questions(self):
        queryCheck = "MATCH (u:User)-[:Follows]->(p:User) WHERE u.username = {username} RETURN count(p)"
        result = graph.run(queryCheck, username = self.username)
        if (result.next()['count(p)'] == 0):
            query = '''
            MATCH (u:User)-[:Asked]->(q:Question)
            WHERE u.username={username}
            WITH COLLECT({ques:q}) AS row1
            MATCH (u:User)-[:Follows]->(:Tag)-[:Tagged]->(q:Question)
            WHERE u.username={username}
            WITH row1+COLLECT({ques:q}) AS row2           
            UNWIND row2 AS row
            WITH row.ques AS q
            RETURN DISTINCT q
            ORDER BY q.timestamp DESC
            LIMIT 10
        '''
        else:
            query = '''
                MATCH (u:User)-[:Asked]->(q:Question)
                WHERE u.username={username}
                WITH COLLECT({ques:q}) AS row1
                MATCH (u:User)-[:Follows]->(:Tag)-[:Tagged]->(q:Question)
                WHERE u.username={username}
                WITH row1+COLLECT({ques:q}) AS row2
                MATCH (u:User)-[:Follows]->(:User)-[:Asked]->(q:Question)
                WHERE u.username={username}
                WITH row2+COLLECT({ques:q}) AS row3
                UNWIND row3 AS row
                WITH row.ques AS q
                RETURN DISTINCT q
                ORDER BY q.timestamp DESC
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
        rel = Relationship(user, 'Bookmarked', question)
        graph.create(rel)

    def remBookmark(self, questionTitle):
        query = '''
                MATCH (u:User)-[r:Bookmarked]->(q:Question)
                WHERE u.username = {username} AND q.title = {question_title}
                DELETE r
                '''
        graph.run(query, username=self.username, question_title=questionTitle)

    def getBookmarked(self, question_title):
        query = "MATCH (u:User)-[:Bookmarked]->(q:Question) WHERE u.username = {username} AND q.title = {questionTitle} return count(q)"
        result = graph.run(query, username=self.username, questionTitle=question_title)
        return result.next()['count(q)']

    def getBookmarkedQuestion(self):
        query = "MATCH (u:User)-[:Bookmarked]->(question:Question) WHERE u.username={username} return question"
        return graph.run(query, username=self.username)

    # def getTopSuggestions(self):
    #     query = '''
    #     MATCH (myself:User)-[f:Follows]-(t1:Tag),
    #     (u:User)-[ans:Answered]-(a:Answer)-[ans2:AnswerTo]-(q:Question)-[tag:Tagged]-(t2:Tag),
    #     (a)-[up:Upvoted]-(b:User)
    #     WHERE t1=t2 AND myself.username = {username}
    #     RETURN u, COUNT(up)
    #     ORDER BY COUNT(up) DESC
    #     LIMIT 4
    #     '''
    #     return graph.run(query, username=self.username)


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
    MATCH (question:Question)<-[:AnswerTo]-(answer:Answer)<-[:Answered]-(u:User) WHERE question.title = {questiontitle} 
	OPTIONAL MATCH (a:Answer{title:answer.title})<-[b:Upvoted]-(:User) RETURN answer.title AS title, u.username AS user, u.pp AS pp, count(b) AS upvotes ORDER BY upvotes DESC
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
