import unittest
from base64 import b64encode

from app import create_app, db
from app.model import User


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def gen_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        response = self.client.get('/api/v1.0/todo-list', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_bad_auth(self):
        # add a user
        u = User(email='test@123.com', username="tester", password='cat')
        db.session.add(u)
        db.session.commit()

        # authenticate with bad password
        response = self.client.get(
            '/api/v1.0/todo-list',
            headers=self.gen_headers('test@123.com', 'hat'))
        self.assertEqual(response.status_code, 401)


# run with 'python -m pytest'
if __name__ == '__main__':
    unittest.main()
