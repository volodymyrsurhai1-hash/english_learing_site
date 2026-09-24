from django.db import models
from apps.users.models import User


class Word(models.Model):
    word = models.CharField(max_length=100, unique=True, db_index=True)

    full_translation = models.JSONField()

    def __str__(self):
        return self.word


class UserWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_words")
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=[
            ("LEARNING", "Learning"),
            ("LEARNED", "learned"),
        ],
        default="LEARNING",
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "word")

    def __str__(self):
        return f"{self.user.email} -> {self.word.word}"
