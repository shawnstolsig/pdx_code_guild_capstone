from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Manager

# automatically create a Manager when User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Manager.objects.create(user=instance, full_name=f'{instance.first_name} {instance.last_name}')
