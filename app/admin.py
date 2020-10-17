from django.contrib import admin

from .forms import (
   CustomUserAdmin
)
from .models import (
    Profile, ProfileBoard, Route, User
)

admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileBoard)
class ProfileBoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass
