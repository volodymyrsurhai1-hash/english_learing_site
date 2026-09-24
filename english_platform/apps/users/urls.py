from django.contrib.auth import views as auth_views
from django.urls import path

from apps.users import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
