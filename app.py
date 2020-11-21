import os
import re
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User, Category, Post
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret-key"
app.config['JWT_SECRET_KEY'] = 'encrypt'

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
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

@app.route('/signup', methods=["POST"])
def signup():
    #Regular expression that checks a valid email
        ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        #Regular expression that checks a valid password
        preg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        # Instancing the a new user
        user = User()
        #Checking email 
        if (re.search(ereg,request.json.get("email"))):
            user.email = request.json.get("email")
        else:
            return "Invalid email format", 400
        #Checking password
        if (re.search(preg,request.json.get('password'))):
            pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
            user.password = pw_hash
        else:
            return "Invalid password format", 400
        #Ask for everything else
        user.name = request.json.get("name")
        user.age = request.json.get("age")
        user.bio = request.json.get("bio")
 
        db.session.add(user)

        db.session.commit()

        return jsonify({"success": True}), 201

@app.route('/login', methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Email not found"}), 404
    
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify({
            "access_token": access_token,
            "user" : user.serialize(),
            "success": True
        }), 200



if __name__ == "__main__":
    manager.run()