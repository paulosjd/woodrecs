from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_temporary = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'auth_user'
