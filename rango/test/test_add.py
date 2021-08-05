from django.shortcuts import render
from django.test import TestCase
from django.urls import reverse

from rango.models import *


def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    return category


class AddCategoryPageTest(TestCase):

    def test_add_category(self):
        # basically, test add a new category means test if the category use the save method in a right way
        # we test if the slug is correctly automatic generated
        # and will the category model do changes if a category with negative views and likes was added
        category = add_category('Test Category', -1, -2)
        category.save()

        self.assertEqual(category.slug, 'test-category')
        self.assertEqual((category.views >= 0), True)
        self.assertEqual((category.likes >= 0), True)

    def test_add_page(self):
        # to test add a new page, except for the no-negative views test
        # we mainly test if the save method is used in a right way
        category = Category.objects.get_or_create(name='Action')[0]
        page = Page(category=category, title='Test Page', url='http://123.com', views=-100)
        page.save()

        self.assertEqual((page.views >= 0), True)
        self.assertEqual(page.title, 'Test Page')
        self.assertEqual(page.category, category)
        self.assertEqual(page.url, 'http://123.com')