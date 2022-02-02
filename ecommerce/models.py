from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=64, help_text='Enter product name')
    publishing_date = models.DateField(help_text='Enter the product publishing date')
    description = models.TextField(blank=True, null=True, help_text='Enter a description for the product')
    pic = models.ImageField(db_column='Image', blank=True, null=True, help_text='Select a picture for the product',upload_to="products/images/", default="/products/images/a68924_9c96bfe7821a45f391444d6f903809b9mv2.jpeg")
    
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, help_text='Enter a product category')
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL, help_text='Enter a product genre')
    developer = models.ForeignKey(Developer, null=True, on_delete=models.SET_NULL,
                                  help_text='Enter the product developer')
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL,
                                  help_text='Enter the product publisher')

    class Meta:
        ordering = ['name', '-publishing_date']
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class Key(models.Model):
    serial_key = models.CharField(unique=True, max_length=64, help_text='Enter the serial key')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Enter the price for the key')
    sale = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                       help_text='Enter the sale value')
    sale_expiry_date = models.DateTimeField(blank=True, null=True)
    sold = models.BooleanField(default=False)
    
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['product', 'serial_key']
        verbose_name_plural = 'Keys'

    def __str__(self):
        return self.serial_key

    def get_absolute_url(self):
        return reverse('key-detail', args=[str(self.id)])


class Transaction(models.Model):
    # Payment method allowed for transaction
    visa = 'VISA'
    mastercard = 'MASTERCARD'
    maestro = 'MAESTRO'
    paypal = 'PAYPAL'

    PAY_METHOD = [
        (visa, 'Visa'),
        (mastercard, 'MasterCard'),
        (maestro, 'Maestro'),
        (paypal, 'PayPal'),
    ]

    # Transaction states allowed
    success = 'SUCCESS'
    pending = 'PENDING'
    failure = 'FAILURE'

    STATES = [
        (success, 'Success'),
        (pending, 'Pending'),
        (failure, 'Failure'),
    ]

    date_time = models.DateTimeField(blank=True, auto_now_add=True)
    payment_method = models.CharField(choices=PAY_METHOD, blank=True, null=True, max_length=16,
                                      help_text='Choose the payment method')
    state = models.CharField(choices=STATES, default='Pending', max_length=16)
    key = models.OneToOneField(Key, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='customer')
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='seller')

    class Meta:
        unique_together = (('id', 'key'),)
        ordering = ['-date_time']
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return self.key.__str__()

    def get_absolute_url(self):
        return reverse('transaction-detail', args=[str(self.id)])
