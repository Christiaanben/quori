from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

#url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
#username = os.environ.get('neo4j')
#password = os.environ.get('password')

graph = Graph("http://localhost:7474/db/data/",user='neo4j', password='1234') #connects to db when db authetication is off
#graph = Graph(url + '/db/data/', username=username, password=password)
#graph = Graph('http://localhost:7474', username = 'neo4j', password = 'password')

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
        self.username + '\' AND b.id = \' ' + id + '\' CREATE (a)-[r:Upvoted]->(b)'
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
        +self.username +'\' AND b.username = \'' + username +'\' DELETE r'
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

	def editBio(self, bio):
		query = 'MATCH (a:User) WHERE a.username = {username} SET a.bio = {bio}'
		graph.run(query, username=self.username, bio=bio)
		# MATCH (a:User)
		# WHERE a.username = 'Maan'
		# SET a.bio = 'My new bio!'

        def editPassword(self, passwordOld, passwordNew):
            if (verify_password(self, passwordOld)):
                query = 'MATCH (a:User) WHERE a.username = \''
                + self.username + '\' SET a.password = \''
                + bcrypt.encrypt(passwordNew) + '\''
                graph.run(query)
                return true
            # MATCH (a:User)
            # WHERE a.username = 'Maan'
            # SET a.password = 'badPassword42'
            else:
                return False

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
            user = Node('User', username=self.username, password=bcrypt.encrypt(password), bio="I have questions:)!", pp = 'temp.jpg')
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


    def ask(self, title, question, tags):
        user = self.find()
        question = Node(
            'Question',
            title=title,
            id=str(uuid.uuid4()),
            description=question,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, 'Asked', question)
        graph.create(rel)

        tags = [x.strip() for x in tags.split(',')]
        for name in set(tags):
            tag = graph.find_one('Tag', 'title', name)

            rel = Relationship(tag, 'Tagged', question)
            graph.create(rel)

    def get_questions(self):
        query = '''
            MATCH (user:User)-[:Follows]->(:Tag)-[:Tagged]->(question:Question)
            WHERE user.username = {username}
            RETURN question ORDER BY question.timestamp
            LIMIT 5
            UNION  MATCH (user:User)-[:Follows]->(p:User)-[:Asked]->(question:Question)
            WHERE user.username = {username}
            RETURN question ORDER BY question.timestamp
            LIMIT 5
        '''
        return graph.run(query, username = self.username)

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

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')
