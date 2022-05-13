from http import client
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from customer.models import Profile, Wishlist


class UserTestCase(TestCase):
    def setUp(self):
            self.user_example = {
                'first_name': 'Account',
                'last_name': 'Test',
                'username': 'User_test',
                'email': 'test_user@test.com',
                'password': 'Pokemonroberto5'
            }
            user = User.objects.create_user(**self.user_example)
            Profile.objects.create(user=user)
            Wishlist.objects.create(user=user)

    def test_create_user(self):
        response = self.client.post('/signup', {
            'first_name': 'Victoria',
            'last_name': 'Blake',
            'username': 'vblake',
            'email': 'vblake@test.com',
            'password1' : 'Prova123',
            'password2' : 'Prova123'
        }, follow=True)
        self.assertRedirects(response, '/')
        self.assertIsNotNone(User.objects.get(username='vblake'))

    def test_create_existing_user(self):
        self.user_example['password1'] = 'Pokemonroberto5'
        self.user_example['password2'] = 'Pokemonroberto5'
        response = self.client.post('/signup', self.user_example)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email and/or password don\'t match')
        
    def test_create_user_pass_mismatch(self):
        response = self.client.post('/signup', {
            'first_name': 'Jake',
            'last_name': 'Seller',
            'username': 'jsell',
            'email': 'jsell@test.com',
            'password1' : 'Pokemonroberto5',
            'password2' : 'Pokemonroberto6'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email and/or password don\'t match')

    def test_user_login(self):
        response = self.client.post('/accounts/login/', {
            'username': self.user_example['username'],
            'password': self.user_example['password']
            })
        self.assertRedirects(response, '/')

    def test_user_login_with_wrong_password(self):
        response = self.client.post('/accounts/login/', {
            'username': self.user_example['username'],
            'password': 'Prova123'
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username and/or password')
        
    def test_user_login_with_not_existing_username(self):
        response = self.client.post('/accounts/login/', {
            'username': 'NotExist',
            'password': self.user_example['password']
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username and/or password')
