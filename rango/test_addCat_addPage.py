from django.test import TestCase
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
