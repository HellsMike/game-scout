from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False, help_text='Check if user is seller')
    picture = models.ImageField(blank=True, null=True, help_text='Select a profile picture')

    class Meta:
        ordering = ['user']
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])
