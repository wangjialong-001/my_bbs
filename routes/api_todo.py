import json
from flask import (
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from utils import log

from routes import *

from models.todo import Todo


#  创建蓝图,相当于路由字典
main = Blueprint('api_todo', __name__)



# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
@main.route("/all")
def all():
    """
    返回所有 todo
    """
    todo_list = Todo.all()
    # 要转换为 dict 格式才行
    todos = [t.json() for t in todo_list]
    return jsonify(todos)


@main.route("/add", methods=["POST"])
def add():
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并返回给浏览器
    """
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 todo
    t = Todo.new(form)
    # 把创建好的 todo 返回给浏览器
    return jsonify(t.json())



@main.route('/delete')
def delete():
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    """
    id = int(request.args.get('id'))
    t = Todo.delete(id)
    return jsonify(t.json())


@main.route('/update', methods=['POST'])
def update():
    form = request.get_json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return jsonify(t.json())
