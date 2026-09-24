from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(blank=True)
    video_file = models.CharField(max_length=500)
    subtitle_en = models.CharField(max_length=500, blank=True)
    subtitle_ru = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
