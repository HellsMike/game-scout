from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True, null=True, help_text='Select a profile picture')
    sold_keys = models.PositiveIntegerField(blank=True, null=True, default=0, help_text="Number of keys sold by this user")
    seller_ratings_count = models.PositiveIntegerField(blank=True, null=True, default=0, help_text="Number of ratings given to this user")
    seller_total_ratings = models.PositiveIntegerField(blank=True, null=True, default=0)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])
