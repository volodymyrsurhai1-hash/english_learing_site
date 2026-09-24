from django.urls import path

from apps.cards import views

app_name: str = "cards"

urlpatterns = [
    path("", views.FlashcardRedirectView.as_view(), name="index"),
    path("<int:pk>/", views.FlashcardView.as_view(), name="card"),
    path("<int:pk>/learned/", views.MarkLearnedView.as_view(), name="learned"),
]
