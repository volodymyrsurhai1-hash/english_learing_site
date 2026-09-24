from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from two_factor.urls import urlpatterns as tf_urls

from apps.core.views import serve_media_with_range

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.users.urls")),
    path("", include("apps.dictionary.urls", namespace="dictionary")),
    path("cards/", include("apps.cards.urls", namespace="cards")),
    path("grammar/", include("apps.grammar.urls", namespace="grammar")),
    path("films/", include("apps.films.urls", namespace="films")),
    path('', include(tf_urls)),
]

if settings.DEBUG:
    media_url = settings.MEDIA_URL.lstrip("/")
    urlpatterns += [
        re_path(
            rf"^{media_url}(?P<path>.*)$",
            serve_media_with_range,
            name="media_serve",
        ),

    ]
