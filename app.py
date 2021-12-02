"""Blogly application."""

from flask import Flask, render_template, request
# from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from models import db, connect_db, User
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


@app.route('/users')
def list_users():
  '''Show the list of all the users in database'''
  users = User.query.all()
  return render_template('list.html', users=users)


@app.route('/users/new')
def show_form():
  '''Show the create a user form'''
  return render_template('form.html')

@app.route('/users/new', methods=['POST'])
def create_user():
  '''Create a user form'''
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
  return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
  '''Show edit user page'''
  user = User.query.get_or_404(user_id)
  return render_template('edit.html', user=user)

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