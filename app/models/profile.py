from django.db import models

from .managers.profile_manager import ProfileManager
from .user import User


class Profile(models.Model):
    """ A model representing a User. Links to their activity and data. """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    email_confirmed = models.BooleanField(
        default=False,
    )
    birth_year = models.IntegerField(
        default=0,
        blank=True
    )
    height = models.IntegerField(
        default=0,
        help_text='Height in cm',
        blank=True
    )
    # TODO - remove the two below - not used anymore ?
    board_width = models.IntegerField(
        help_text='Number of holds(x)',
        default=8,
    )
    board_height = models.IntegerField(
        help_text='Number of holds(y)',
        default=11,
    )

    objects = ProfileManager()

    def __str__(self):
        return self.user.username + '_profile'
