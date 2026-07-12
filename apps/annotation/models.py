from django.db import models
from django.conf import settings


class UploadedImage(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="uploads/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.image.name
class Polygon(models.Model):

    image = models.ForeignKey(
        UploadedImage,
        on_delete=models.CASCADE,
        related_name="polygons"
    )

    label = models.CharField(
        max_length=100,
        blank=True
    )

    points = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Polygon {self.id}"