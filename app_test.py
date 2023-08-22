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

    # def test_register_new_user(self):
    #     response = self.app.post('/register', data={'username': 'TestA', 'password': 'Pass123?'}, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     expected_url = "/"
    #     self.assertEqual(response.request.path, expected_url)

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

    def test_add_record(self):
        response = self.app.post('/televisions/add', data={
            'brand': 'Sony',
            'audio': 'Stereo',
            'resolution': '4K',
            'refresh_rate': '60 Hz',
            'screen_size': '55 inches'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/televisions')

    def test_add_record_with_bad_chars(self):
        response = self.app.post('/televisions/add', data={
            'brand': 'Sony',
            'audio': 'Stereo?',
            'resolution': '4K',
            'refresh_rate': '60 Hz',
            'screen_size': '55 inches'
        })
        self.assertEqual(response.status_code, 400)
        expected_url = "/televisions/add"
        self.assertEqual(response.request.path, expected_url)
        expected_error_message = "Invalid characters or length detected."
        self.assertIn(expected_error_message.encode(), response.data)

    def test_update_record_as_regular_in_session(self):
        response = self.app.post('/televisions/edit/submit', data={
            'tv_id': 1,
            'brand': 'LG',
            'audio': 'Dolby Digital',
            'resolution': '1080p',
            'refresh_rate': '120 Hz',
            'screen_size': '65 inches'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/televisions')

    def test_delete_record_as_regular(self):
        response = self.app.get('/admin/televisions/delete', query_string={'tv_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/home')

    def test_update_record_as_admin(self):
        response = self.app.post('/login', data={'username': 'admin', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/televisions/edit/submit', data={
            'tv_id': 2,
            'brand': 'LG',
            'audio': 'Dolby Digital',
            'resolution': '1080p',
            'refresh_rate': '120 Hz',
            'screen_size': '65 inches'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/televisions')

    def test_delete_record_as_admin(self):
        response = self.app.post('/login', data={'username': 'admin', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/admin/televisions/delete', query_string={'tv_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/televisions')


if __name__ == '__main__':
    unittest.main()
