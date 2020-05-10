from django.contrib import admin

from app.service.models import Restaurant, Menu, Order, Meal, Address, MealType

models = (
    Restaurant,
    Menu,
    Order,
    Meal,
    MealType,
    Address
)

admin.site.register(models)
