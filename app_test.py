import unittest
from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def test_login_valid_user(self):
        response = self.app.post('/login', data={'username': 'admin', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        expected_url = "/home"
        self.assertEqual(response.request.path, expected_url)
        expected_text = "Welcome, " + "admin"
        self.assertIn(expected_text.encode(), response.data)

    def test_login_unregistered_user(self):
        response = self.app.post('/login', data={'username': 'anotheradmin', 'password': 'Pass123?'},
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        expected_text = "Invalid username or password. Please try again."
        self.assertIn(expected_text.encode(), response.data)

    def test_register_new_user(self):
        response = self.app.post('/register', data={'username': 'TestA', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        expected_url = "/"
        self.assertEqual(response.request.path, expected_url)

    def test_register_with_bad_username(self):
        response = self.app.post('/register', data={'username': 'Test', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        expected_url = "/register"
        self.assertEqual(response.request.path, expected_url)
        expected_error_message = "Invalid username. Must meet the specified criteria."
        self.assertIn(expected_error_message.encode(), response.data)

    def test_register_with_bad_password(self):
        response = self.app.post('/register', data={'username': 'TestB', 'password': 'Pass'}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        expected_url = "/register"
        self.assertEqual(response.request.path, expected_url)
        expected_error_message = "Invalid password. Must meet the specified criteria."
        self.assertIn(expected_error_message.encode(), response.data)


if __name__ == '__main__':
    unittest.main()
