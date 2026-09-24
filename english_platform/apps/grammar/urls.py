from django.urls import path

from apps.grammar import views

app_name = "grammar"

urlpatterns = [
    path("", views.GrammarListView.as_view(), name="list"),
    path("my/", views.MyGrammarListView.as_view(), name="my_list"),
    path(
        "my/delete/<slug:slug>/", views.DeleteTopicView.as_view(), name="delete_topic"
    ),
    path("add/", views.AddTopicView.as_view(), name="add_topic"),
    path("<slug:slug>/", views.GrammarDetailView.as_view(), name="detail"),
]
