from django.urls import path

from apps.dictionary import views

app_name: str = "dictionary"

urlpatterns = [
    path("", views.SearchView.as_view(), name="search"),
    path("save/", views.SaveWordView.as_view(), name="save_word"),
    path("delete/", views.DeleteWordView.as_view(), name="delete_word"),
    path("toggle/", views.ToggleWordStatusView.as_view(), name="toggle_word"),
]
