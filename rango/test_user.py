# Unit Test for user related function: login, register etc
# To execute this test: python manage.py test rango.test_user

from django.test import TestCase
import tempfile
from rango.models import Category, User, UserProfile
from rango.forms import UserForm, UserProfileForm
from django.forms import fields as django_fields
from django.db import models
from django.urls import reverse

import os, os.path

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

# ----------------------------------------------------#
# Test cases for User Register
# ----------------------------------------------------#
class RegisterFormClassTests(TestCase):
    def test_user_form(self):
        """
        Tests whether UserForm has correct fields and the fields have been specified.
        """
        user_form = UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAILURE_HEADER}UserForm does not match up to the User model. Please check it.{FAILURE_FOOTER}")

        fields = user_form.fields

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserForm form. Please check it.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

    def test_user_profile_form(self):
        """
        Tests whether UserProfileForm is created and whether the correct fields have been specified for it.
        """
        user_profile_form = UserProfileForm()
        self.assertEqual(type(user_profile_form.__dict__['instance']), UserProfile, f"{FAILURE_HEADER}UserProfileForm does not match up to the UserProfile model. Please check it.{FAILURE_FOOTER}")

        fields = user_profile_form.fields

        expected_fields = {
            'website': django_fields.URLField,
            'picture': django_fields.ImageField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserProfile form. Please check it.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")
