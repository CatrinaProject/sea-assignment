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

    # This test is commented out as the test fails if username 'TestA' already exists
    # def test_register_new_user(self):
    #     response = self.app.post('/register', data={'username': 'TestA', 'password': 'Pass123?'}, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     expected_url = "/"
    #     self.assertEqual(response.request.path, expected_url)

    def test_register_with_bad_username(self):
        response = self.app.post('/register', data={'username': 'Test', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        expected_url = "/"
        self.assertEqual(response.request.path, expected_url)
        expected_error_message = "User input failed to pass Username regex validation"
        self.assertIn(expected_error_message.encode(), response.data)

    def test_register_with_bad_password(self):
        response = self.app.post('/register', data={'username': 'TestB', 'password': 'Pass'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        expected_url = "/"
        self.assertEqual(response.request.path, expected_url)
        expected_error_message = "User input failed to pass Password regex validation"
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
        self.assertEqual(response.headers['Location'], '/televisions')

    def test_update_record(self):
        response = self.app.post('/televisions/edit/submit', data={
            'tv_id': 2,
            'brand': 'LG',
            'audio': 'Dolby Digital',
            'resolution': '1080p',
            'refresh_rate': '120 Hz',
            'screen_size': '65 inches'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/televisions')

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
        self.assertEqual(response.headers['Location'], '/televisions')

    def test_delete_record(self):
        response = self.app.get('/admin/televisions/delete', query_string={'tv_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/home')

    def test_delete_record_as_admin(self):
        response = self.app.post('/login', data={'username': 'admin', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/admin/televisions/delete', query_string={'tv_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/televisions')

    def test_admin_dashboard_as_admin(self):
        response = self.app.post('/login', data={'username': 'admin', 'password': 'Pass123?'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
        expected_url = "/admin/dashboard"
        self.assertEqual(response.request.path, expected_url)
        expected_text = "Admin Approvals"
        self.assertIn(expected_text.encode(), response.data)

    def test_admin_dashboard_as_regular(self):
        response = self.app.post('/admin/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/home')

# Create a test suite
test_suite = unittest.TestLoader().loadTestsFromTestCase(AppTestCase)

# Run the test suite
test_runner = unittest.TextTestRunner()
test_result = test_runner.run(test_suite)

# Access results
print("Number of tests run:", test_result.testsRun)
print("Number of failures:", len(test_result.failures))
print("Number of errors:", len(test_result.errors))

if __name__ == '__main__':
    unittest.main()
