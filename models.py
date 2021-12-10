"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
  '''Connect to database'''
  db.app = app 
  db.init_app(app)


class User(db.Model):
  '''User'''
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  first_name = db.Column(db.String, nullable = False)
  last_name = db.Column(db.String, nullable = False)
  image_url = db.Column(db.String, nullable = False, default='https://upload.wikimedia.org/wikipedia/commons/7/7e/Circle-icons-profile.svg')

  posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
  '''Post'''
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  title = db.Column(db.String, nullable = False)
  content = db.Column(db.Text, nullable = False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  @property
  def friendly_date(self):
      """Return nicely-formatted date."""

      return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):
  '''Post tag'''
  __tablename__ = 'post_tags'
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False, primary_key=True)

class Tag(db.Model):
  '''Tag'''
  __tablename__='tags'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  name = db.Column(db.Text, nullable=False, unique=True)

  posts = db.relationship("Post",secondary='post_tags', backref="tags")#, cascade="all, delete-orphan")

