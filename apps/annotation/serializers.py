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

    image = serializers.SerializerMethodField()

    class Meta:
        model = UploadedImage
        fields = "__all__"
        read_only_fields = (
            "user",
            "uploaded_at",
        )

    def get_image(self, obj):
        if not obj.image:
            return None

        url = obj.image.url
        if url.startswith(("http://", "https://")):
            return url

        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(url)

        return url