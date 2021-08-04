import unittest, sys, os

sys.path.append('../Climate-Change')
from main import app, db
from main import User

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    ###############
    #### tests ####
    ###############

# Test register-
    def register(self, username, email, password):
        return self.app.post('/register',
                            data=dict(username=username,
                                      email=email,
                                      password=password, 
                                      confirm_password=password),
                            follow_redirects=True)

    def test_valid_user_registration(self):
        response = self.register('test', 'test', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_username_registration(self):
        response = self.register('t', 'test@example.com', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)

    def test_invalid_email_registration(self):
        response = self.register('test2', 'test@example', 'FlaskIsAwesome')
        self.assertIn(b'Invalid email address.', response.data)

# Test adding new users to database-        
    def test_add_user(self):
        lucas=User(username="lucas", email="lucas@example.com", password="test")
        user2 = User(username="lucas", email="lucas@test.com")

        db.session.add(lucas)
        db.session.commit()

        assert lucas in db.session
        assert user2 not in db.session
        
#   Test login-         
    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username,
                                      password=password),
                            follow_redirects=True)
    
    def test_valid_login(self):
        valid_user=User(username="testuser", email="email@example.com", password="test2")
        db.session.add(valid_user)
        
        response=self.login('testuser','test2')
        self.assertEqual(response.status_code, 200)
        
#     def test_invalid_login(self):
#         response=self.login('person22','password2')
# #         print(response.data)
#         self.assertIn(b'Login Unsuccessful. Please check email and password', response.data)

        
        

if __name__ == "__main__":
    unittest.main()