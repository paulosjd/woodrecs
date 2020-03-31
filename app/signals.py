from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Profile
from woodrecs import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """ Creates a Profile instance when a User instance is created """
    if created:
        profile = Profile.objects.create(user=instance)
        # send_verification_email.delay(instance.pk)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """ Updates a Profile instance when a User instance is updated """
    instance.profile.save()
