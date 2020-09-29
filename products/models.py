from django.db import models
from django.contrib.auth.models import User
from profiles.models import SellerProfile, ClientProfile
from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
import numpy as np
import math
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
# from django.db import models
# Create your models here.


def upload_location(instance, filename, **kwargs):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


class Categories(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    UNITS = (
        ('K', ('Kilogram')),
        ('G', ('Gram')),
        ('L', ('Liter')),
    )
    STOCK_STATUS = (
        ('IN-STOCK', ('IN-STOCK')),
        ('OUT OF STOCK', ('OUT OF STOCK')),
    )
    DELIVERY_DAYS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
    )
    MAX_DELIVERY_DAYS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
    )
    unit = models.CharField(max_length=150, choices=UNITS,
                            default='K', blank=True, null=True)
    title = models.CharField(max_length=150)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, default=None)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField(default=False, null=True, blank=False)
    minorder = models.IntegerField(
        help_text='Minum Products that want to sell on per order', null=True, default=None, blank=True)
    image = models.ImageField()
    delivery_days = models.IntegerField(
        choices=DELIVERY_DAYS, blank=True, null=True, help_text='Select Minimum Delivery Days')
    max_delivery_days = models.IntegerField(
        choices=MAX_DELIVERY_DAYS,  blank=True, null=True, help_text='Select Maximum Delivery Days')
    category = models.ForeignKey(
        Categories, default=1, on_delete=models.CASCADE)
    deal_status = models.BooleanField(
        default=False,  help_text='Check this for dispalying on home page')
    deal_price = models.FloatField(
        null=True, blank=True)
    stock_status = models.CharField(max_length=150, choices=STOCK_STATUS,
                                    default='IN-STOCK')
    slug = models.SlugField(blank=True, unique=True)

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(list(all_ratings))

    def __str__(self):
        return self.title

    @property
    def get_price(self):
        price = self.price
        return price

    @property
    def get_deal_price(self):
        deal_price = self.deal_price
        return deal_price


def pre_save_product_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user.username + "-" + instance.title)


pre_save.connect(pre_save_product_post_receiever, sender=Product)


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(
        choices=RATING_CHOICES)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    STATUSFORBUYER = (
        ('Not-Received', 'Not-Received'),
        ('Received', 'Received'),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUS, default='Pending')
    statusforbuyer = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUSFORBUYER, default='Not-Received')

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitem)
        return total

    @property
    def get_deal_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum(item.get_deal_total for item in orderitem)
        return total

    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum(item.quantity for item in orderitem)
        return total


class OrderItem(models.Model):
    STATUS = (
        ('0', '0'),
        ('1', '1'),
    )
    STATUSFORSELLER = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    STATUSFORBUYER = (
        ('Not-Received', 'Not-Received'),
        ('Received', 'Received'),
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    feedback_status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUS)
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUSFORSELLER, default='Pending')
    statusforbuyer = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUSFORBUYER, default='Not-Received')

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        price = self.product.price
        quantity = self.quantity
        total = price*quantity
        print(total)

        return total

    @property
    def get_deal_total(self):
        price = self.product.deal_price
        quantity = self.quantity
        total = price*quantity
        print(total)

        return total


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=150)
    date_orderd = models.DateTimeField(auto_now_add=True)
    ph_number = models.CharField(
        validators=[MinLengthValidator(11)], max_length=11)

    def __str__(self):
        return self.address


class Wishlist(models.Model):
    # here CASCADE is the behavior to adopt when the referenced object(because it is a foreign key) is deleted. it is not specific to django,this is an sql standard.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wished_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wished_item.title
