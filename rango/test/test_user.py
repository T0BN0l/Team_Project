from django.test import TestCase
from rango.models import Category, User, UserProfile
from django.urls import reverse

import os, os.path

# Create your tests here.

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

# ----------------------------------------------------#
# Helper functions used in test case
# ----------------------------------------------------#
def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

def create_super_user_object():
    """
    Helper function to create a super user (admin) account.
    """
    return User.objects.create_superuser('admin', 'admin@test.com', 'adminpassword')

# ----------------------------------------------------#
# Test cases for User Login
# ----------------------------------------------------#
class UserLoginTests(TestCase):
    """
    Tests to check whether the UserProfile model has been created and
    """
    def test_userlogin(self):
        user = create_user_object()
        self.assertTrue(self.client.login(username='testuser', password='testabc123'), \
            f"{FAILURE_HEADER}We couldn't log our sample user in during the tests. Please check your implementation of UserForm and UserProfileForm.{FAILURE_FOOTER}")

    def test_login_functionality(self):
        """
        Tests the login functionality. A user should be able to log in, and should be redirected to the Rango homepage.
        """
        user_object = create_user_object()

        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'testabc123'})

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Testing your login functionality, logging in was successful. However, we expected a redirect; we got a status code of {response.status_code} instead. Check your login() view implementation.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('rango:index'), f"{FAILURE_HEADER}We were not redirected to the Rango homepage after logging in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

    def test_menus_display(self):
        """
        Checks to see if the menus required authentification displayed when a user logs in.
        """
        content = self.client.get('/rango/').content.decode()
        self.assertTrue('Login' in content, f"{FAILURE_HEADER}We didn't see login for a user not logged in on the Rango homepage. Please check your index.html template.{FAILURE_FOOTER}")
        self.assertFalse('Logout' in content, f"{FAILURE_HEADER}Before logging in, Logout menu should not be displayed. Check your index.html template.{FAILURE_FOOTER}")
        self.assertFalse('Profile' in content, f"{FAILURE_HEADER}Before logging in, Profile menu should not be displayed. Check your index.html template.{FAILURE_FOOTER}")

        create_user_object()
        self.client.login(username='testuser', password='testabc123')

        content = self.client.get('/rango/').content.decode()
        self.assertFalse('Login' in content, f"{FAILURE_HEADER}After logging a user, Login menu should not be displayed. Check your index.html template.{FAILURE_FOOTER}")
        self.assertTrue('Logout' in content, f"{FAILURE_HEADER}After logging a user, Logout menu should be displayed. Check your index.html template.{FAILURE_FOOTER}")
        self.assertTrue('Profile' in content, f"{FAILURE_HEADER}After logging a user, Profile menu should be displayed. Check your index.html template.{FAILURE_FOOTER}")