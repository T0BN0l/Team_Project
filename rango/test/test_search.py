from django.test import TestCase
from rango.models import *
from rango.views import *
from django.test import Client


def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category


class UserLoginTests(TestCase):
    def test_empty(self):
        response = self.client.get('/rango/suggest/', {'suggestion': ''})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], [])
        self.assertContains(response, "There are no categories present.")

    def test_search(self):
        cat01 = add_category("Test01", 10, 10)
        cat02 = add_category("test02", 11, 11)
        cat03 = add_category("test03", 12, 12)
        cat04 = add_category("BBB01", 13, 14)
        cat05 = add_category("ttt01", 15, 16)

        response = self.client.get('/rango/suggest/', {'suggestion': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test01")
        self.assertContains(response, "test02")
        self.assertContains(response, "test03")
        self.assertEqual(len(response.context['categories']), 3)

        response = self.client.get('/rango/suggest/', {'suggestion': ''})
        self.assertEqual(len(response.context['categories']), 5)

        response = self.client.get('/rango/suggest/', {'suggestion': 't'})
        self.assertEqual(len(response.context['categories']), 4)

        response = self.client.get('/rango/suggest/', {'suggestion': 'b'})
        self.assertEqual(len(response.context['categories']), 1)