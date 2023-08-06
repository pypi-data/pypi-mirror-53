from django.urls import reverse
from django.db import models

from .base import BaseSink


class ArchieDoc(BaseSink):
    title = models.CharField(
        "Document title", max_length=250, help_text="A title for this doc"
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="archie_docs",
    )

    def serialize(self):
        return {
            "id": self.google_id,
            "title": self.title,
            "publish": reverse(
                "kitchensink-publish-archie-doc", args=[self.id]
            ),
            "type": "doc",
            "project": self.project.title if self.project else None,
        }

    def __str__(self):
        return self.title
