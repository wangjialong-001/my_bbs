from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.topic import Topic
from models.board import Board
from models.user import User


main = Blueprint('topic', __name__)


import uuid
csrf_tokens = set()

@main.route("/")
def index():
    # board_id = 2
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    board = Board.get(m.board_id)
    u = User.get(m.user_id)
    board_title = board.title
    username = u.username
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, board_title=board_title, username=username)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    t = Topic.get(id)
    token = request.args.get('token')
    u = current_user()
    # 判断 token 是否是我们给的
    if token in csrf_tokens:
        csrf_tokens.remove(token)
        if u.id == t.user_id:
            print('删除 topic 用户是', u, id)
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)
