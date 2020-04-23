from datetime import datetime

from django.db import models

from app.authentication.models import CoreUser
from app.cabinet.models import Address
from app.utils.utils import generate_random_string


def upload_user_avatar_image(instance, filename):
    d, rand_str = datetime.now(), generate_random_string(15)
    return f'storage/avatars/{d.year:04d}-{d.month:02d}/{rand_str}{filename}'


class Meal(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_user_avatar_image, null=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'meals'


class Order(models.Model):
    status = models.CharField(max_length=191)
    courier = models.IntegerField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name='orders')
    cost = models.FloatField()
    meal = models.ForeignKey(Meal, models.DO_NOTHING, related_name='meal_order')

    class Meta:
        db_table = 'orders'


class Restaurant(models.Model):
    menu = models.IntegerField()
    address = models.ForeignKey(Address, models.DO_NOTHING, related_name='restaurants')

    class Meta:
        db_table = 'restaurants'
