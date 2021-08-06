from django.test import TestCase
from rango.models import *
from rango.views import *


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


def create_user_profile(user):
    """
    Helper function to create a UserProfile object.
    """
    profile = UserProfile.objects.get_or_create(user=user,
                                                website='https://www.google.com',
                                                picture='/static/images/rango.jpg')[0]
    return profile


class UserProfileTest(TestCase):
    def test_user_profile(self):
        testuser = create_user_object()
        create_user_profile(testuser)

        self.assertEqual(ProfileView.get_user_details(self, username=testuser.username)[1].website, 'https://www.google.com')
        self.assertEqual(ProfileView.get_user_details(self, username=testuser.username)[1].picture, '/static/images/rango.jpg')


    def test_update_website(self):
        testuser = create_user_object()
        create_user_profile(testuser)

        UserProfile.objects.update(user_id=testuser.id,
                                   user=testuser,
                                   website='https://github.com')

        self.assertEqual(ProfileView.get_user_details(self, username=testuser.username)[1].website, 'https://github.com')


    def test_update_picture(self):
        testuser = create_user_object()
        create_user_profile(testuser)

        UserProfile.objects.update(user_id=testuser.id,
                                   user=testuser,
                                   picture='/static/images/uofg.jpg')

        self.assertEqual(ProfileView.get_user_details(self, username=testuser.username)[1].picture, '/static/images/uofg.jpg')
