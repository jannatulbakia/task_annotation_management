from django.contrib import admin
from .models import UploadedImage, Polygon


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "uploaded_at")
    search_fields = ("user__email",)
    ordering = ("-uploaded_at",)


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "label", "created_at")
    search_fields = ("label",)
    ordering = ("-created_at",)