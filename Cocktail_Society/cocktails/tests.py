from django.test import TestCase

from .models import Cocktail
from accounts.models import Account


# Create your tests here.
class TestLikes(TestCase):

    def test_cocktails_likes(self):
        testuser1 = Account.objects.create_user(email='razraz@company.com',
                                                first_name='user1_name',
                                                last_name='user1_lastname',
                                                username='user1',
                                                password='password')
        testuser2 = Account.objects.create_user(email='razdwa@company.com',
                                                first_name='user2_name',
                                                last_name='user2_lastname',
                                                username='user2',
                                                password='password')
        cocktail = Cocktail.objects.create(cocktail_name='my_own',
                                               cocktails_category='alc',
                                               crockery_category='short',
                                               method_category='stir',
                                               ingredients='rum',
                                               execution='test',
                                               image='cocktail.png',
                                               created='2020-12-20')
        cocktail.likes.set([testuser1.pk, testuser2.pk])
        self.assertEqual(cocktail.likes.count(), 2)
