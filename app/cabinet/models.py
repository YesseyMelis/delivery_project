from django.db import models

from app.authentication.models import CoreUser
from app.service.models import Meal


class Address(models.Model):
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name='address', null=True)
    name = models.CharField(max_length=191)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    z_coordinate = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'address'


class Wallet(models.Model):
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name='wallet_user')
    address = models.CharField(unique=True, max_length=191)
    name = models.CharField(max_length=191, blank=True, null=True)
    status = models.IntegerField()
    balance = models.DecimalField(max_digits=56, decimal_places=4, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'wallet'


class Basket(models.Model):
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name='basket')
    meal = models.ForeignKey(Meal, models.DO_NOTHING, related_name='meal_basket')
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'baskets'
