from django.contrib import admin

from app.service.models import Restaurant, MenuSubscription, Menu, Order, Meal

models = (
    Restaurant,
    MenuSubscription,
    Menu,
    Order,
    Meal,
)

admin.site.register(models)
