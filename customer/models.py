from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True, null=True, help_text='Select a profile picture')

    class Meta:
        verbose_name_plural = 'Profiles'
    #
    # u = user.forward_related_accessor_class
    # u = User.objects.get(id=1).get_username()
    # print(u)
    # print(type(u))
    # def get_user(self):
    #     u = User.get_username()
    #     return u
    #

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])
