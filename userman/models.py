from django.db import models


class Customer(models.Model):
    id_user = models.UUIDField(primary_key=True, unique=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    e_mail = models.EmailField(unique=True)
    pic = models.ImageField(blank=True, default='')
    seller = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Customers'
