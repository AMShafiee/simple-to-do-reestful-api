import unittest
import requests
from requests.auth import HTTPBasicAuth
from app import create_app, db
from config import Config
from app.models import User, Role, Project, Task
from werkzeug.security import generate_password_hash, check_password_hash


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user1 = User(first_name='Rose', last_name='Johnson', username='rose',
                     password_hash=generate_password_hash('my_secret_pass', method='sha256'))
        db.session.add(user1)
        db.session.commit()
        self.assertFalse(check_password_hash(
            user1.password_hash, 'a_mistake_pass'))
        self.assertTrue(check_password_hash(
            user1.password_hash, 'my_secret_pass'))

    def test_user(self):
        user1 = User(username='rose', first_name='Rose', last_name='Johnson')
        user2 = User(username='mark', first_name='Mark', last_name='Smith')
        db.session.add_all([user1, user2])
        db.session.commit()
        self.assertEqual(User.query.filter_by(
            username='rose').first().last_name, 'Johnson')

        # response = requests.post("http://localhost:5000/auth/signup",
        #                          data={"first_name": 'Rose', "last_name": 'Johnson', "role": "manager",
        #                                "username": 'rose', "password": "my_secret_pass"})
        # print(response.json()['message'])
        # self.assertTrue(response.json()['was_successful'])
        # response = requests.post("http://localhost:5000/auth/signup",
        #                          data={"first_name": 'Mark', "last_name": 'Smith', "role": "developer",
        #                                "username": 'mark', "password": "another_pass"})
        # print(response.json()['message'])
        # self.assertTrue(response.json()['was_successful'])

        response = requests.post("http://localhost:5000/auth/login",
                                 data={"username": 'mark', "password": "another_pass"})
        print("\n"+response.json()['message'])
        print(response.json()['data'])
        self.assertTrue(response.json()['was_successful'])
        response = requests.post("http://localhost:5000/auth/login",
                                 data={"username": 'rose', "password": "my_secret_pass"})
        print(response.json()['message'])
        print(response.json()['data'])
        self.assertTrue(response.json()['was_successful'])
        response = requests.post("http://localhost:5000/auth/login",
                                 data={"username": 'Rose', "password": "my_secret_pass"})
        print(response.json()['message'])
        self.assertFalse(response.json()['was_successful'])

    def test_task(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
