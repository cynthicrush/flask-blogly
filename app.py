"""Blogly application."""

from flask import Flask, render_template, request
# from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from models import db, connect_db, User, Post
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhh-secret'

# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
  '''Show the list of all the users in database'''
  return redirect('/users')

# Users route

@app.route('/users')
def list_users():
  '''Show the list of all the users in database'''
  users = User.query.all()
  return render_template('users/list.html', users=users)


@app.route('/users/new')
def show_add_user_form():
  '''Show the create a user form'''
  return render_template('users/form.html')

@app.route('/users/new', methods=['POST'])
def create_user():
  '''Create a user'''
  first_name = request.form['first-name']
  last_name = request.form['last-name']
  image_url = request.form['image-url']

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  pdb.set_trace()
  db.session.commit()

  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
  '''Show user details'''
  user = User.query.get_or_404(user_id)
  # posts = Post.query.get(user_id)
  return render_template('users/details.html', user=user)#, posts=posts

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
  '''Show edit user page'''
  user = User.query.get_or_404(user_id)
  return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
  '''Show edit user page'''
  user = User.query.get_or_404(user_id)
  user.first_name = request.form['first-name']
  user.last_name = request.form['last-name']
  user.image_url = request.form['image-url']

  db.session.add(user)
  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  '''Delete a user'''
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/users')

# Posts route

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
  '''Show the add post form'''

  user = User.query.get_or_404(user_id)
  return render_template('posts/form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
  '''Create a post'''
  user = User.query.get_or_404(user_id)
  new_post = Post(title=request.form['title'], 
                  content=request.form['content'], 
                  user_id=user.id)

  db.session.add(new_post)
  db.session.commit()
  
  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
  '''Show details of a post'''

  post = Post.query.get(post_id)

  return render_template('posts/details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_from(post_id):
  '''Show the form to edit a post'''

  post = Post.query.get(post_id)
  render_template('posts/edit.html', post=post)