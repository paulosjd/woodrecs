from datetime import datetime
from operator import itemgetter
from typing import List, Optional

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
    gender = models.CharField(
        choices=[('', ' '), ('m', 'Male'), ('f', 'Female')],
        default='',
        max_length=1,
        blank=True
    )
    objects = ProfileManager()

    @property
    def age(self) -> Optional[int]:
        if self.birth_year:
            return datetime.now().year - self.birth_year

    def __str__(self):
        return self.user.username + '_profile'
