from django.db.models.signals import post_save
from django.dispatch import receiver

from app.authentication.models import CoreUser
from app.cabinet.models import Basket


@receiver(post_save, sender=CoreUser)
def create_basket(sender, instance, created, **kwargs):
    if created:
        Basket.objects.create(
            user=instance
        )