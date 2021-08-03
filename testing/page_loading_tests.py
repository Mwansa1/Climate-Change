from flask import Flask
import unittest, sys

sys.path.append('../QuickASL') # imports python file from parent directory
from main import app #imports flask app object

class page_loading_tests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_home_page(self):
        response = self.app.get('/home', follow_redirects=True)
        response2 = self.app.get('/', follow_redirects=True)

        self.assertEqual(response.status_code and response2 , 200)
        
        
    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_logout_page(self):
        response = self.app.get('/logout', follow_redirects= True)
        self.assertEqual(response.status_code, 200)
    
    def test_suggestions_page(self):
        response = self.app.get('/suggestions', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_show_user_list_page(self):
        response = self.app.get('/list', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_createpost(self):
        response = self.app.get('/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_posts_(self):
        response = self.app.get('/posts', follow_redirects=True)
        self.assertEqual(response.status_code, 200)     
        


        
        



if __name__ == "__main__":
    unittest.main()