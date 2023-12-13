from django.db import models
from django.conf import settings


class Room(models.Model):

    name = models.CharField(max_length=100)  # duplicated

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.name}"
