from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_userprofile(sender, created, instance, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)


@receiver(post_delete, sender=UserProfile)
def delete_related_user(sender, instance, **kwargs):
    instance.user.delete()


