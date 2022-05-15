from datetime import datetime
from zoneinfo import ZoneInfo
from django.test import TestCase
from django.contrib.auth.models import User, Group
from customer.models import Profile, Wishlist
from ecommerce.models import Category, Developer, Genre, Product, Publisher, Key


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


class KeyManagerTestCase(TestCase):
    def setUp(self):
        self.user_example = User.objects.create_user(
            first_name = 'Account',
            last_name = 'Test',
            username = 'User_test',
            email = 'test_user@test.com',
            password = 'Pokemonroberto5'
            )
        Profile.objects.create(user=self.user_example)
        Wishlist.objects.create(user=self.user_example)
        group = Group.objects.get_or_create(name='Sellers')[0]
        self.user_example.groups.add(group)
        self.client.post('/accounts/login/', {
            'username': 'User_test',
            'password': 'Pokemonroberto5'
            })
        
        genre = Genre.objects.create(name='Genre_test')
        developer = Developer.objects.create(name='Developer_test')
        publisher = Publisher.objects.create(name='Publisher_test')
        category = Category.objects.create(name='Category_test')
        self.product_example = Product.objects.create(  
            name = 'Test_product',
            publishing_date = '2000-01-01',
            genre = genre,
            category = category,
            developer = developer,
            publisher = publisher
            )
        self.key_example = {
            'product': self.product_example.name,
            'serial_key': '0000',
            'price': '10',
            'sale': '',      
            'seller': self.user_example.id,
        }
        
    def add_key(self):
        return Key.objects.create(
            product = self.product_example,
            serial_key = self.key_example['serial_key'],
            price = self.key_example['price'],
            sale_price = self.key_example['price'],      
            seller = self.user_example
            )
        
    def test_add_key(self):
        response = self.client.post('/add-key', self.key_example, follow=True)
        self.assertRedirects(response, '/keymanager')
        user = response.context['user']
        self.assertEqual(Key.objects.filter(seller=user).count(), 1)
        response = self.client.get('/keymanager', self.key_example, follow=True)
        self.assertContains(response, f'{self.product_example.name}')
    
    def test_remove_key(self):
        key = self.add_key()
        first_count = Key.objects.filter(seller=key.seller).count()
        response = self.client.post('/delete-key', {'key_id_to_delete': key.id}, follow=True)
        self.assertRedirects(response, '/keymanager')
        self.assertEqual(Key.objects.filter(seller=key.seller).count(), first_count-1)
    
    def test_update_key(self):
        key = self.add_key()
        updated_values = {
            'choose_key_modify': key.id,
            'serial_key': '1111',
            'price': '20',
            'sale': '20',
            'sale_expiry_date': datetime(2025, 1, 1, 00, 00, 00, 000000, tzinfo=ZoneInfo("Europe/Rome"))
            }
        response = self.client.post('/modify-key', updated_values, follow=True)
        self.assertRedirects(response, '/keymanager')
        new_key = Key.objects.get(id=key.id)
        self.assertNotEqual(key.serial_key, new_key.serial_key)
        self.assertNotEqual(key.price, new_key.price)
        self.assertNotEqual(key.sale, new_key.sale)
        self.assertNotEqual(key.sale_price, new_key.sale_price)
        self.assertNotEqual(key.sale_expiry_date, new_key.sale_expiry_date)
