from unittest import TestCase
from app import app
from models import db, User
import pdb

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUT_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.debug = False

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
  '''Tests for views for pets.'''

  def setUp(self):
    '''Adding a sample user'''

    User.query.delete()

    user = User(first_name='TestUserFirstName', last_name='TestUserLastName', image_url='https://upload.wikimedia.org/wikipedia/commons/7/7e/Circle-icons-profile.svg')
    db.session.add(user)
    db.session.commit()

    self.user_id = user.id
  
  def tearDown(self):
    '''Clean up any fouled transaction.'''

    db.session.rollback()

  def test_list_users(self):
    with app.test_client() as client:
      response = client.get('/')
      html = response.get_data(as_text=True)

      self.assertEqual(response.status_code, 200)
      self.assertIn('TestUserFirstName TestUserLastName', html)

  def test_show_user(self):
    with app.test_client() as client:
      response = client.get(f'/users/{self.user_id}')
      html = response.get_data(as_text=True)

      self.assertEqual(response.status_code, 200)
      self.assertIn('<h1>TestUserFirstName TestUserLastName</h1>', html)

  def test_add_user(self):
    with app.test_client() as client:
      data = {'first_name': 'TestUserFirstName2', 'last_name': 'TestUserLastName2', 'image_url': 'https://www.pngall.com/wp-content/uploads/5/Profile-PNG-Clipart.png'}
      response = client.get('/users', data=data, follow_redirects=True)
      pdb.set_trace()
      html = response.get_data(as_text=True)

      self.assertEqual(response.status_code, 200)
      self.assertIn('TestUserFirstName2 TestUserLastName2', html)

