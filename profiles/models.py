from django.db import models
from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator

# Create your models here.


class SellerProfile(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE, default=None)
    mobileNo = models.CharField(
        validators=[MinLengthValidator(11)], max_length=11, default=None)
    # cnic = models.CharField(max_length=13,
    #                         validators=[MinLengthValidator(13)])
    city = models.CharField(max_length=30, default=None)
    address = models.CharField(max_length=30, default=None)
    state = models.CharField(max_length=30, default=None)
    shop_name = models.CharField(max_length=30, default=None)
    profile_pic = models.ImageField(
        null=True, blank=True, default="default.png")

    def __str__(self):
        return self.user.username


class ClientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
