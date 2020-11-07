from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20))

    def __repr__(self):
        return "<User %r>" % self.name
    
    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "age":self.age,
            "gender": self.gender
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return "<Post %r>" % self.title
    
    def serialize(self):
        return {
            "id":self.id,
            "title":self.title,
            "body": self.body,
            "publication_date":self.publication_date,
            "category_id":self.category_id,
            "user_id": self.user_id
        }
        

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return "<Category %r>" % self.name
    
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
        }
            

    