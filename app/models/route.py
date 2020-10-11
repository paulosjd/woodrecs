from django.core.exceptions import ValidationError
from django.db import models

from app.models.managers.route_manager import RouteManager


class Route(models.Model):

    grade_choices = ['6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b',
                     '7b+', '7c', '7c+', '8a']

    name = models.CharField(
        max_length=50,
        help_text='e.g. Body weight',
    )
    grade = models.CharField(
        max_length=3,
        default='',
    )
    # Need save validate that '5,7,9,...' maps with xholds to give ...
    x_holds = models.CharField(
        max_length=50,
        verbose_name='Hold sequence',
        help_text="Comma-separated list of holds, e.g. 'A4,D3,E5,G5,K6'",
    )
    y_holds = models.CharField(
        max_length=50,
        verbose_name='Hold sequence',
        help_text="Comma-separated list of holds, e.g. 'A4,D3,E5,G5,K6'",
    )
    ticked = models.BooleanField(
        default=False
    )
    notes = models.CharField(
        max_length=120,
        default='',
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

    def save(self, **kwargs):
        print(self.x_holds)
        if len(str(self.x_holds).split(',')) != len(
                str(self.x_holds).split(',')):
            raise ValidationError('split len holds mismatch')
        super(Route, self).save(**kwargs)
