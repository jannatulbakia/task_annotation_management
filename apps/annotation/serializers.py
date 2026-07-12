from rest_framework import serializers
from .models import UploadedImage, Polygon


class PolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = "__all__"


class UploadedImageSerializer(serializers.ModelSerializer):

    polygons = PolygonSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = UploadedImage
        fields = "__all__"
        read_only_fields = (
            "user",
            "uploaded_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            url = instance.image.url
            if not url.startswith(("http://", "https://")):
                request = self.context.get("request")
                if request:
                    url = request.build_absolute_uri(url)
            data["image"] = url
        return data