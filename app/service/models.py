from datetime import datetime

from django.db import models

from app.authentication.models import CoreUser
from app.utils.utils import generate_random_string


def upload_user_avatar_image(instance, filename):
    d, rand_str = datetime.now(), generate_random_string(15)
    return f'storage/images/{d.year:04d}-{d.month:02d}/{rand_str}{filename}'


class Address(models.Model):
    name = models.CharField(max_length=191)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    z_coordinate = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return self.name


class MealType(models.Model):
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'meal_types'

    def __str__(self):
        return self.name


class Meal(models.Model):
    category = models.ForeignKey(MealType, on_delete=models.DO_NOTHING, related_name='meals')
    name = models.CharField(max_length=191, blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', null=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'meals'

    def __str__(self):
        return self.name


class Order(models.Model):
    PROCESS = 'process'
    CONFIRMED = 'confirmed'
    DELIVERED = 'delivered'
    STATUS_CHOICE = (
        (PROCESS, PROCESS),
        (CONFIRMED, CONFIRMED),
        (DELIVERED, DELIVERED)
    )
    status = models.CharField(max_length=191, choices=STATUS_CHOICE, default=PROCESS)
    courier = models.ForeignKey(CoreUser, models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name='orders')
    meals = models.ManyToManyField(Meal)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    @property
    def cost(self):
        ms = self.meals.all().values_list('price', flat=True)
        o_cost = 0
        for price in ms:
            o_cost += price
        return o_cost


class Menu(models.Model):
    name = models.CharField(max_length=191, null=True, blank=True)
    meals = models.ManyToManyField(Meal)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'menu'
        verbose_name_plural = 'Menu'

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=191, null=True, blank=True)
    menu = models.ForeignKey(Menu, models.DO_NOTHING, related_name='restaurants')
    address = models.ForeignKey(Address, models.DO_NOTHING, related_name='restaurants')
    work_time = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'restaurants'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name


class MenuSubscription(models.Model):
    menu = models.ForeignKey(Menu, models.DO_NOTHING, related_name='menu_subscriptions')
    meal = models.ForeignKey(Meal, models.DO_NOTHING, related_name='subscriptions')
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'menu_subscriptions'
        verbose_name = 'Menu Subscription'
        verbose_name_plural = 'Menu Subscriptions'
