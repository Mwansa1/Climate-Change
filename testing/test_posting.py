import unittest, sys, os
from unittest.mock import Mock

sys.path.append('../Climate-Change')
from main import app, db
from main import User, Posts

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
#         test_user= User(username="user1", email="email@example.com", password="password")

        
        
    ###############
    #### tests ####
    ###############

    def test_create_post(self):
        test_user= User(username="user1", email="email@example.com", password="password")
        post = Posts(title='test title', content='Example content', author=test_user)
        
        db.session.add(post)
        db.session.commit()
        
        is_in_db=False
        invalid_post = Posts(title='tji83i', content='content', author=test_user)
        if (invalid_post in db.session):
            is_in_db = True
        
        print(is_in_db)

        assert post in db.session
#         self.assertFalse(is_in_db)
        
    def test_delete_valid_post(self):
        test_user= User(username="user1", email="email@example.com", password="password")
        db.session.add(User)
        db.session.commit()
        
        post = Posts(title='valid title', content='something', author=test_user)
        db.session.add(post)
        db.session.commit()

        db.session.delete(post)
        db.session.commit()
        
        assert post not in db.session
        
# test delete post that doesnt exist
#     def test_delete_invalid_post(self):
#         test_post= Posts(title='something', content="something")
#         db.session.delete(test_post)
#         db.session.commit()
#         assert error
        
        



        

if __name__ == "__main__":
    unittest.main()