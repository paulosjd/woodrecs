from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class ProfileBoard(models.Model):

    board_dim = models.CharField(
        max_length=4,
        help_text='For board dimension of 11 x 8, expect "1108"',
        validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='nomatch')],
        db_index=True,
    )
    hold_set = models.CharField(
        max_length=500,
        help_text="JSON string of hold set data",
    )
    profile = models.ForeignKey(
        'app.Profile',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('board_dim', 'profile')

    def __str__(self):
        return f'ProfileBoard: {self.profile} - {self.board_dim}'

    def save(self, **kwargs):
        # if upload_fields_len != self.num_values + 1:
        #     raise ValidationError('split upload_field_labels and')
        super(ProfileBoard, self).save(**kwargs)
