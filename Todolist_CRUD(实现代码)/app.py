import flask
from flask import Flask, request,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import config

app = Flask(__name__)
app.secret_key = "asd"
app.config.from_object(config)
db = SQLAlchemy(app)

migrate = Migrate(app,db)

class List(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),nullable=False)
    state = db.Column(db.String(200), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime, default=datetime.now)

#user = List(title="123",code="133")
with app.app_context():
    db.create_all()

@app.route("/add/",methods=["POST"])#增加
def add_list():
    my_json = request.get_json()
    print(my_json)
    get_title = my_json.get("title")
    data = List(title=get_title,state="unfinished")
    db.session.add(data)
    db.session.commit()
    return jsonify(code=200,msg="success")

@app.route("/query/",methods=["POST"])#查询所有数据
def query_list1():
    data = List.query.all()
    for i in data:
        print("title: "+i.title+" state: "+i.state)
    return jsonify(code=200,msg="success")

@app.route("/id_query/",methods=["POST"])#按id查询数据
def query_list2():
    my_json = request.get_json()
    print(my_json)
    get_id = my_json.get("id")
    data = List.query.filter_by(id=get_id).first()
    print("title: "+data.title+" state: "+data.state)
    return jsonify(code=200,msg="success")

@app.route("/finished_query/",methods=["POST"])#查询已完成数据
def query_list3():
    data = List.query.filter_by(state="unfinished")
    for i in data:
        print("title: " + i.title + " state: " + i.state)
    return jsonify(code=200,msg="success")

@app.route("/unfinished_query/",methods=["POST"])#查询未完成数据
def query_list4():
    data = List.query.filter_by(state="finished")
    for i in data:
        print("title: " + i.title + " state: " + i.state)
    return jsonify(code=200,msg="success")

@app.route("/keyword_query/",methods=["POST"])#关键字查询
def query_list5():
    my_json = request.get_json()
    print(my_json)
    q = my_json.get("title")
    data = List.query.filter(List.title.contains(q))
    for i in data:
        print("title: " + i.title + " state: " + i.state)
    return jsonify(code=200,msg="success")

@app.route("/finished/",methods=["POST"])#更改一条为已完成
def update_list1():
    my_json = request.get_json()
    print(my_json)
    get_id = my_json.get("id")
    list=List.query.filter_by(id=get_id).first()
    list.state="finished"
    db.session.commit()
    return jsonify(code=200,msg="success")


@app.route("/unfinished/",methods=["POST"])#更改为未完成
def update_list2():
    my_json = request.get_json()
    print(my_json)
    get_id = my_json.get("id")
    list=List.query.filter_by(id=get_id).first()
    list.state="unfinished"
    db.session.commit()
    return jsonify(code=200,msg="success")

@app.route("/finish_all/",methods=["POST"])#更改所有为已完成
def update_list3():
    data = List.query.all()
    for i in data:
        i.state = "finished"
    db.session.commit()
    return jsonify(code=200,msg="success")

@app.route("/unfinish_all/",methods=["POST"])#更改所有为未完成
def update_list4():
    data = List.query.all()
    for i in data:
        i.state = "unfinished"
    db.session.commit()
    return jsonify(code=200,msg="success")



@app.route("/delete/",methods=["POST"])#根据给定id删除一条数据
def delete_list1():
    my_json = request.get_json()
    print(my_json)
    get_id = my_json.get("id")
    list = List.query.filter_by(id=get_id).first()
    db.session.delete(list)
    db.session.commit()
    return jsonify(code=200,msg="success")

@app.route("/delete_all/",methods=["POST"])#删除所有
def delete_list2():
    data = List.query.all()
    for i in data:
        db.session.delete(i)
    db.session.commit()
    return jsonify(code=200,msg="success")

@app.route("/delete_finished/",methods=["POST"])#删除已完成
def delete_list3():
    data = List.query.filter_by(state="finished")
    for i in data:
        db.session.delete(i)
    db.session.commit()
    return jsonify(code=200, msg="success")

@app.route("/delete_unfinished/",methods=["POST"])#删除未完成
def delete_list4():
    data = List.query.filter_by(state="unfinished")
    for i in data:
        db.session.delete(i)
    db.session.commit()
    return jsonify(code=200, msg="success")


# 学习
#
# @app.route("/test/",methods=["POST"])
# def test():
#
#     try:
#         my_json = request.get_json()
#         print(my_json)
#         get_name = my_json.get("name")
#         get_age = my_json.get("age")
#         print(get_name)
#         if not all([get_age,get_name]):
#             return jsonify(msg="缺少参数")
#         get_age += 10
#         return jsonify(name=get_name, age=get_age)
#     except Exception as e:
#         print(e)
#         return jsonify(msg="出错了，请查看是否正确访问")
# @app.route("/login/",methods=["POST"])
# def login():
#     my_json = request.get_json()
#     print(my_json)
#     get_name = my_json.get("name")
#     get_password = my_json.get("password")
#     print(get_name)
#     if not all([get_name, get_password]):
#         return jsonify(msg="参数不完整")
#
#     if get_name == "asd123" and get_password == "asd":
#         session["name"] = get_name
#         return jsonify(msg="登录成功")
#     else:
#         return jsonify(msg="账号或密码错误")
#
#
#
#
# @app.route("/session/",methods=["GET"])
# def check():
#     username = session.get("name")
#     if username is not None:
#         return jsonify(username=username)
#     else:
#         return jsonify(msg="出错了")
#
# @app.route("/logout/",methods=["GET"])
# def logout():
#     session.clear()
#     return jsonify(msg="退出登录成功")

if __name__ == '__main__':
    app.run()