from django.urls import path

from .views.board_setup import BoardSetupView
from .views.problems import ProblemsView
from .views.profile_data import ProfileDataView
from .views.user import (
    DeleteUserView, EmailEditView, LoginHelp,
    PasswordReset, RegistrationAPIView, NewVerificationEmail
)

urlpatterns = [
    path('users/confirm-delete', DeleteUserView.as_view()),
    path('users/email/edit', EmailEditView.as_view()),
    path('users/help/<forgot>', LoginHelp.as_view()),
    path('users/new-verification-email', NewVerificationEmail.as_view()),
    path('users/password-reset', PasswordReset.as_view()),
    path('users/registration', RegistrationAPIView.as_view()),
    path('profile/board-setup', BoardSetupView.as_view()),
    path('profile/problems', ProblemsView.as_view()),
    path('profile/data', ProfileDataView.as_view(), name='profile_data'),
]
