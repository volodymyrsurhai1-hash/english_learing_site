from django.urls import path

from apps.dictionary import views

app_name: str = "dictionary"

urlpatterns = [
    path("", views.SearchView.as_view(), name="search"),
]
