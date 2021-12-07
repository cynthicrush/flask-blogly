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
  first_name = db.Column(db.String(), nullable = False)
  last_name = db.Column(db.String(), nullable = False)
  image_url = db.Column(db.String(), nullable = False, default='https://upload.wikimedia.org/wikipedia/commons/7/7e/Circle-icons-profile.svg')

class Post(db.Model):
  '''Post'''
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  title = db.Column(db.String(), nullable = False)
  content = db.Column(db.Text(), nullable = False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
  user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
