import flask
import mongoengine
from mongoengine import Document, IntField, StringField, ReferenceField
from flask import Flask, render_template, request

mongoengine.connect(db='chan') # uses default (localhost:27017)
app = Flask(__name__)

class Board(Document):
    shortname = StringField(unique=True)
    name = StringField(unique=True)

    @staticmethod
    def getdict():
        build = {}
        objs = Board.objects()
        for obj in objs: build[obj.shortname] = obj.name
        return build

class Post(Document):
    id = IntField(primary_key=True, unique=True)
    body = StringField()
    image = StringField()
    board = ReferenceField(Board)
    replyingto = IntField()
    name = StringField(default='anon')

'''
post = Post(id=6969, body="", image="", ) # How to format a post
post.save() #Saving the post

# Get all posts from board g
Post.objects(board=Board.object(shortname="g")[0])

newboard = Board(shortname='k', name='weapons') # Submit new board
Board.objects().to_json() # Get all boards
'''

initboards = {'g':'technology', 'b':'random', 'gif':'gif', 'hr':'high res'}
if Board.objects().count() == 0:
    for board in initboards:
        board = Board(shortname=board, name=initboards[board])
        board.save()

@app.route('/')
def index():
    boards = Board.getdict()
    print(boards)
    return render_template('index.html', boards = boards)

@app.route('/<board>')
def board(board):
    q = Board.objects(shortname=board)
    if q.count() == 0:
        return flask.abort(404)
    return render_template('board.html', sn=board, board=q[0])

@app.route('/post', methods=['POST'])
def post():
    print(request.data)
    return 'done'

if __name__ == '__main__':
    app.run(debug=True)
