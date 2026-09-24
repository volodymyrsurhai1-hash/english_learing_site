from django.urls import path

from apps.films import views

app_name: str = "films"

urlpatterns = [
    path("", views.FilmListView.as_view(), name="list"),
    path("<int:pk>/", views.FilmWatchView.as_view(), name="watch"),
    path("download/", views.FilmDownloadView.as_view(), name="download"),
    path(
        "api/start-download/", views.StartDownloadView.as_view(), name="start_download"
    ),
    path(
        "api/download-progress/<str:task_id>/",
        views.DownloadProgressView.as_view(),
        name="download_progress",
    ),
    path("api/translate/", views.TranslateWordView.as_view(), name="translate"),
    path("api/save-word/", views.SaveWordFromFilmView.as_view(), name="save_word"),
]
