"""Blogly application."""

from flask import Flask, render_template, request
# from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from models import db, connect_db, User, Post, PostTag, Tag
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
  '''Show homepage'''
  return render_template('/homepage.html')

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
  pdb.set_trace()
  first_name = request.form['first-name']
  last_name = request.form['last-name']
  image_url = request.form['image-url']

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  db.session.commit()

  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
  '''Show user details'''
  user = User.query.get_or_404(user_id)
  # posts = Post.query.get(user_id)
  return render_template('users/details.html', user=user)#, posts=posts

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
  '''Show edit user page'''
  user = User.query.get_or_404(user_id)
  return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
  '''Edit user'''
  user = User.query.get_or_404(user_id)
  user.first_name = request.form['first-name']
  user.last_name = request.form['last-name']
  user.image_url = request.form['image-url']

  db.session.add(user)
  db.session.commit()
  return redirect(f'/users/{user_id}')

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
  tags = Tag.query.all()
  return render_template('posts/form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
  '''Create a post'''
  user = User.query.get_or_404(user_id)
  tag_ids = [int(num) for num in request.form.getlist('tags')]
  tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
  new_post = Post(title=request.form['title'], 
                  content=request.form['content'], 
                  user=user,
                  tags=tags)

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

  post = Post.query.get_or_404(post_id)
  tags = Tag.query.all()
  return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
  '''Edit the post'''

  post = Post.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']

  tag_ids = [int(num) for num in request.form.getlist('tags')]
  post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

  db.session.add(post)
  db.session.commit()
  return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
  '''Delete a post'''

  post = Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()
  return redirect(f'/users/{post.user_id}')

# Tags route

@app.route('/tags')
def list_tags():
  '''List all the tags'''
  tags = Tag.query.all()
  return render_template('tags/list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
  '''Show details of a tag'''
  tag = Tag.query.get_or_404(tag_id)
  return render_template('tags/detail.html', tag=tag)

@app.route('/tags/new')
def show_add_tag_form():
  '''Show the create a tag form'''
  return render_template('tags/form.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
  '''Create a tag'''
  name = request.form['name']

  new_tag = Tag(name=name)
  db.session.add(new_tag)
  db.session.commit()

  return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
  '''Show edit tag form'''
  tag = Tag.query.get_or_404(tag_id)

  return render_template('tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
  '''Edit a tag'''
  tag = Tag.query.get_or_404(tag_id)
  tag.name = request.form['name']

  db.session.add(tag)
  db.session.commit()
  return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
  '''Delete a tag'''
  tag = Tag.query.get_or_404(tag_id)
  db.session.delete(tag)
  db.session.commit()
  return redirect('/tags')