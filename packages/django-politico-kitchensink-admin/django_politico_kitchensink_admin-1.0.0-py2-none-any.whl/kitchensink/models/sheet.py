from django.urls import reverse
from django.db import models

from .base import BaseSink


class Sheet(BaseSink):
    title = models.CharField(
        "Project title", max_length=250, help_text="A title for this sheet"
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="sheets",
    )

    def serialize(self):
        return {
            "id": self.google_id,
            "title": self.title,
            "publish": reverse("kitchensink-publish-sheet", args=[self.id]),
            "type": "sheet",
            "project": self.project.title if self.project else None,
        }

    def __str__(self):
        return self.title
