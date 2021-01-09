from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout-redirect/', LogoutView.as_view(), name='logout-redirect'),
    path('user-profile/', CurrentUserProfileView.as_view(), name='user-profile'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='reset_password'),
    path('password-reset-sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
         name='reset_password_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done'),
         name='password_reset_complete')
]
