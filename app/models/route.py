from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models

from app.models.managers.route_manager import RouteManager


class Route(models.Model):

    grade_choices = ['6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b',
                     '7b+', '7c', '7c+', '8a']

    name = models.CharField(
        max_length=50,
    )
    grade = models.CharField(
        max_length=3,
        default='',
    )
    rating = models.IntegerField(
        blank=True,
        default=0,
    )
    x_holds = models.CharField(
        max_length=50,
        verbose_name='Hold sequence',
        help_text="Comma-separated list of holds, e.g. '03,02,08'",
    )
    y_holds = models.CharField(
        max_length=50,
        verbose_name='Hold sequence',
        help_text="Comma-separated list of holds, e.g. '02,05,07'",
    )
    ticked = models.BooleanField(
        default=False
    )
    notes = models.CharField(
        max_length=120,
        default='',
        blank=True,
    )
    profile_board = models.ForeignKey(
        'app.ProfileBoard',
        on_delete=models.CASCADE,
        related_name='routes',
    )

    objects = RouteManager()

    class Meta:
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Route: {self.name}'

    @staticmethod
    def hold_is_invalid(s):
        if not isinstance(
                s, str) or not s.isdigit() or int(s) not in range(100):
            return True

    def has_hold_error(self) -> Optional[str]:
        for s in str(self.x_holds).split(','):
            if self.hold_is_invalid(s):
                return 'invalid x_hold'
        for s in str(self.y_holds).split(','):
            if self.hold_is_invalid(s):
                return 'invalid y_hold'
        if len(str(self.x_holds).split(',')) != len(
                str(self.x_holds).split(',')):
            return 'split len holds mismatch'

    def save(self, **kwargs):
        hold_error = self.has_hold_error()
        if hold_error:
            raise ValidationError(hold_error)
        super(Route, self).save(**kwargs)
