import os
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User, Category, Post

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand) # init, migrate, upgrade

CORS(app)

@app.route('/user/<int:id>', methods=["GET","DELETE", "PUT"])
@app.route('/user', methods=["POST"])
def user(id=None):
    if id is not None:
        if request.method == "GET":
            user = User.query.filter_by(id=id).first()
            return jsonify(user.serialize()), 200
        
        if request.method == "PUT":
            user = User.query.get(id)
            user.age = request.json.get("age")
            db.session.commit()
            return jsonify(user.serialize()), 200
        
        if request.method == "DELETE":
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg":"User deleted"}), 200
    elif request.method == "POST":
        user = User()
        user.name = request.json.get("name")
        user.age = request.json.get("age")
        user.gender = request.json.get("gender")
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 200

@app.route('/post', methods=["POST"])
def post():
    if request.method == "POST":
        post = Post()
        post.title = request.json.get("title")
        post.body = request.json.get("body")
        post.category_id = request.json.get("category_id")
        post.user_id = request.json.get("user_id")
        db.session.add(post)
        db.session.commit()
        return jsonify(post.serialize()), 200
    else:
        return jsonify({"msg": "Wrong path"}), 400

@app.route('/category', methods=["POST"])
def category():
    category = Category()
    category.name = request.json.get("name")
    db.session.add(category)
    db.session.commit()
    return jsonify(category.serialize()), 200



if __name__ == "__main__":
    manager.run()