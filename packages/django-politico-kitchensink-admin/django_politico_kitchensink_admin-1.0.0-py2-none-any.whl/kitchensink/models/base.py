import uuid

from django.db import models
from foreignform.fields import JSONField


class BaseSink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    google_id = models.SlugField("Google Doc ID", help_text="Doc ID from URL")
    validation_schema = JSONField(
        blank=True, null=True, help_text="JSON Schema"
    )

    VERSION_CHOICES = [("v1", "v1"), ("v2", "v2")]

    version = models.CharField(
        max_length=2,
        choices=VERSION_CHOICES,
        blank=False,
        null=False,
        default="v2",
        help_text="Should be the latest version when created.",
    )

    class Meta:
        abstract = True
