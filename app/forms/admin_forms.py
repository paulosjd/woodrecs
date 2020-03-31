from django import forms
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',
                       'is_temporary')}
         ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        UserAdmin.list_display = (
            'username', 'email', 'first_name', 'last_name', 'is_staff',
            'is_temporary'
        )
