from django.contrib import admin

from app.cabinet.models import Address, Wallet

models = (
    Address,
    Wallet
)

admin.site.register(models)
