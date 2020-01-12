import os
import json
import flask
import mongoengine
from mongoengine import Document, IntField, StringField, ReferenceField
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg', 'gif', 'webm'}

mongoengine.connect(db='chan')  # uses default (localhost:27017)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class Board(Document):
    shortname = StringField(unique=True)
    name = StringField(unique=True)

    @staticmethod
    def getdict():
        build = {}
        objs = Board.objects()
        for obj in objs:
            build[obj.shortname] = obj.name
        return build


class Post(Document):
    body = StringField()
    image = StringField()
    board = StringField()
    replyingto = StringField()
    name = StringField()


'''
post = Post(body="", image="", etc...) # How to format a post
post.save() #Saving the post

# Get all posts from board g
Post.objects(board=Board.object(shortname="g")[0])

newboard = Board(shortname='k', name='weapons') # Submit new board
Board.objects().to_json() # Get all boards
'''


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS


initboards = {'g': 'technology', 'b': 'random', 'gif': 'gif', 'hr': 'high res'}
if Board.objects().count() == 0:
    for board in initboards:
        board = Board(shortname=board, name=initboards[board])
        board.save()


@app.route('/')
def index():
    boards = Board.getdict()
    print(boards)
    return render_template('index.html', boards=boards)


@app.route('/<board>')
def board(board):
    q = Board.objects(shortname=board)
    if q.count() == 0:
        return flask.abort(404)
    threadsobj = Post.objects(board=board)
    print('Threads: '+str(len(threadsobj)))
    threads = {}
    for thread in threadsobj:
        j = {str(thread.id): {'name': thread.name,
                              'body': thread.body, 'image': thread.image}}
        threads.update(j)
    print(threads)
    return render_template('board.html', sn=board, board=q[0], threads=threads)


@app.route('/<board>/<tid>')
def reply(board, tid):
    # Get thread owner
    owner = Post.objects(id=tid)[0]
    ownerdict = {tid: {'name': owner.name,
                       'body': owner.body, 'image': owner.image}}
    # Get all childeren posts
    try:
        replies = Post.objects(replyingto=tid)
        repliesdict = {}
        for reply in replies:
            replydict = {reply.id: {'name': reply.name,
                                    'body': reply.body, 'image': reply.image}}
            repliesdict.update(replydict)
    except:
        repliesdict = {}
    return render_template('replies.html', owner=ownerdict, replies=repliesdict, tid=tid, board=owner.board)

@app.route('/post', methods=['POST'])
def post():
    r = request.form
    if r.get('replyingto'):
        replyingto = r['replyingto']
    else:
        replyingto = 0
    name = r['name']
    body = r['body']
    board = r['board']
    image = ''
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = file.filename
    except:
        print('No file')
    post = Post(body=body, board=board, name=name,
                image=image, replyingto=replyingto)
    post.save()
    return 'done'

@app.route('/boardsubmit', methods=['POST'])
def boardsubmit():
    r = request.form
    boardname = r['boardName']
    boardsn = r['boardShortName']
    print(boardname)
    print(boardsn)
    boards = Board.getdict()
    if boardsn in boards.keys():
        if boardname == boards[boardsn]:
            return 'ERR: a board with that name and shortname already exists'
        else:
            return 'ERR: a board with that shortname exists'
    else:
        newboard = Board(shortname=boardsn, name=boardname)
        newboard.save()
        print('Board '+boardname+' created')
        return 'OKK: Board Created'

if __name__ == '__main__':
    app.run(debug=True)
