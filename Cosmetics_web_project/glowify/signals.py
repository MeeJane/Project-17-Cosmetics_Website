from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wishlist, Cart


@receiver(post_save, sender=User)
def create_user_assets(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)
        Cart.objects.create(user=instance)
