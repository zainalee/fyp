from django.db import models
from products.models import Categories
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator


class PostRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(PostRequest, on_delete=models.CASCADE)
    description = models.CharField(
        validators=[MinLengthValidator(20)], max_length=250)
    price = models.IntegerField()
    contact_number = models.CharField(
        validators=[MinLengthValidator(11)], max_length=11)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.contact_number
