from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

#url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
#username = os.environ.get('neo4j')
#password = os.environ.get('password')

#graph = Graph(url + '/db/data/', username=username, password=password)
graph = Graph('http://localhost:7474', username = 'neo4j', password = 'password')

class User:
    def __init__(self, username):
        self.username = username
        
    def addFollows(self, username):
        query = '''MATCH (a:User),(b:User)
        WHERE a.username = \' ''' + self.username + '''\' AND b.username = \'''' + username + '''\'
		CREATE (a)-[r:Follows]->(b)'''
        return graph.run(query)
        # MATCH (a:User),(b:User)
		# WHERE a.username = 'Ricky' AND b.username = 'Maan'
		# CREATE (a)-[r:Follows]->(b)
        
    def addUpvoted(self, id):
        query = 'MATCH (a:Person), (b:Answer) WHERE a.username = \''
        self.username + '\' AND b.id = \' ' + id + '\' CREATE (a)-[r:Upvoted]->(b)'    	
        return graph.run(query)
        # MATCH (a:User),(b:User)
		# WHERE a.username = 'Ricky' AND b.id = 'A2'
		# CREATE (a)-[r:Upvoted]->(b)
        

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

    def find(self):
        user = graph.exists(Node('User', 'username', self.username))
        return user

    def register(self, password):
        if not self.find():
            user = Node('User', username=self.username, password=bcrypt.encrypt(password))
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

    def ask_question(self, id, title, description, tags):
        user = self.find()
        q = Node('Question', 
            id=id, 
            title = title, 
            description = description, 
            timestamp=timestamp(), 
            date=date())
        rel = Relationship(user, 'Asked', q)
        graph.create(rel)
        for name in tags:
            tag = Node('Tag', title=name)
            graph.merge(tag)

            rel = Relationship(tag, 'Tagged', q)
            graph.create(rel)


    def add_post(self, title, tags, text):
        user = self.find()
        post = Node(
            'Post',
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, 'PUBLISHED', post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = Node('Tag', name=name)
            graph.merge(tag)

            rel = Relationship(tag, 'TAGGED', post)
            graph.create(rel)

    def get_recent_posts(self):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = {username}
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 5
        '''

        return graph.run(query, username=self.username)

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
