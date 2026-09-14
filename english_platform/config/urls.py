from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.users.urls")),
    path("", include("apps.dictionary.urls", namespace="dictionary")),
]
