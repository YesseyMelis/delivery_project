from django.contrib import admin

from app.cabinet.models import Address, Wallet, Basket, BasketSubscription

models = (
    Address,
    Wallet,
    Basket,
    BasketSubscription,
)

admin.site.register(models)
