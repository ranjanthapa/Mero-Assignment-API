from django.urls import path
from . import views
app_name = "account"

urlpatterns = [
    path("create-account", views.UserView.as_view()),
    path("login", views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('reset-password', views.PasswordResetView.as_view()),
    path("reset-password/confirm", views.PasswordResetConfirmView.as_view(), name="confirm_reset_password")
]