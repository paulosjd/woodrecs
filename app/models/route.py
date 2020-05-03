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
    sequence = models.CharField(
        max_length=50,
        verbose_name='Hold sequence',
        help_text="Comma-separated list of holds, e.g. 'A4,D3,E5,G5,K6'",
    )
    created_by = models.ForeignKey(
        'app.Profile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='custom_routes',
    )

    objects = RouteManager()

    class Meta:
        # unique_together = ('name', 'profile')
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Route: {self.name}'

    def save(self, **kwargs):
        # if upload_fields_len != self.num_values + 1:
        #     raise ValidationError('split upload_field_labels and')
        super(Route, self).save(**kwargs)
