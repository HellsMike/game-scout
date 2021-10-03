from django.db import models
from django.core.validators import MaxValueValidator

import userman.models


class Product(models.Model):
    id_game = models.UUIDField(primary_key=True, unique=True)
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=32)
    developer = models.CharField(max_length=64)
    publisher = models.CharField(max_length=64)
    publishing_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    pic = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Products'


class Key(models.Model):
    id_key = models.UUIDField(primary_key=True, unique=True)
    serial_key = models.CharField(unique=True, max_length=64)
    game = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(userman.models.Customer, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    sold = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Keys'


# Payment method allowed for transaction
PAY_METHOD = [
    ('Visa', 'Visa'),
    ('MasterCard', 'MasterCard'),
    ('Maestro', 'MasterCard'),
    ('PayPal', 'PayPal'),
    ('PaySafeCard', 'PaySafeCard'),
]

STATES = [
    ('Success', 'Success'),
    ('Pending', 'Pending'),
    ('Failure', 'Failure'),
]


class Transaction(models.Model):
    id_trans = models.UUIDField(unique=True)
    key = models.ForeignKey(Key, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    payment_method = models.CharField(choices=PAY_METHOD, blank=True, null=True, max_length=16)
    state = models.CharField(choices=STATES, default='Pending', max_length=16)

    class Meta:
        verbose_name_plural = 'Transactions'
        unique_together = (('id_trans', 'key'),)
