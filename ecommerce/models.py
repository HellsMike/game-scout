from django.db import models
from django.core.validators import MaxValueValidator
from django.urls import reverse

from customer.models import Profile


class Category(models.Model):
    name = models.CharField(unique=True, max_length=64, help_text='Enter a product category (e.g. OS, game)')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=64, help_text='Enter a product genre')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class Developer(models.Model):
    name = models.CharField(unique=True, max_length=64, help_text='Enter a product developer')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Developers'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class Publisher(models.Model):
    name = models.CharField(unique=True, max_length=64, help_text='Enter a product publisher')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class Product(models.Model):
    # id_product = models.UUIDField(primary_key=True, unique=True)
    name = models.CharField(max_length=64, help_text='Enter product name')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, help_text='Enter a product category')
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL, help_text='Enter a product genre')
    developer = models.ForeignKey(Developer, null=True, on_delete=models.SET_NULL,
                                  help_text='Enter the product developer')
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL,
                                  help_text='Enter the product publisher')
    publishing_date = models.DateField(help_text='Enter the product publishing date')
    description = models.TextField(blank=True, null=True, help_text='Enter a description for the product')
    pic = models.ImageField(blank=True, null=True, help_text='Select a picture for the product')

    class Meta:
        ordering = ['name', '-publishing_date']
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def get_product_name(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class Key(models.Model):
    # id_key = models.UUIDField(primary_key=True, unique=True)
    serial_key = models.CharField(unique=True, max_length=64, help_text='Enter the serial key')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # seller = models.ForeignKey(userman.models.Customer, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Enter the price for the key')
    sale = models.PositiveIntegerField(default=0, blank=True, validators=[MaxValueValidator(100)],
                                       help_text='Enter the sale value')
    sold = models.BooleanField(default=False)

    class Meta:
        ordering = ['product', 'serial_key']
        verbose_name_plural = 'Keys'

    def __str__(self):
        return self.serial_key

    def get_absolute_url(self):
        return reverse('key-detail', args=[str(self.id)])


class Transaction(models.Model):
    # Payment method allowed for transaction
    PAY_METHOD = [
        ('Visa', 'Visa'),
        ('MasterCard', 'MasterCard'),
        ('Maestro', 'Maestro'),
        ('PayPal', 'PayPal'),
        ('PaySafeCard', 'PaySafeCard'),
    ]

    # Transaction states allowed
    STATES = [
        ('Success', 'Success'),
        ('Pending', 'Pending'),
        ('Failure', 'Failure'),
    ]

    # id = models.BigAutoField(primary_key=True)
    key = models.OneToOneField(Key, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    payment_method = models.CharField(choices=PAY_METHOD, blank=True, null=True, max_length=16,
                                      help_text='Choose the payment method')
    state = models.CharField(choices=STATES, default='Pending', max_length=16)

    class Meta:
        unique_together = (('id', 'key'),)
        ordering = ['-date', '-time']
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return self.key.__str__()

    def get_absolute_url(self):
        return reverse('transaction-detail', args=[str(self.id)])


class Wishlist(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    wish = models.JSONField()

    class Meta:
        verbose_name_plural = 'Wishlists'
    #
    # def get_username(self):
    #     return self.user.name
    #

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse('wishlist-detail', args=[str(self.id)])


class Order(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    order_list = models.JSONField()

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])
