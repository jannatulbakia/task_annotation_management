from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import UploadedImage, Polygon
from .serializers import (
    UploadedImageSerializer,
    PolygonSerializer,
)
class ImageListCreateView(generics.ListCreateAPIView):

    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(
    user=self.request.user
).order_by("-uploaded_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ImageDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(
            user=self.request.user
        )
        
class PolygonListCreateView(generics.ListCreateAPIView):

    serializer_class = PolygonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Polygon.objects.filter(
            image__user=self.request.user
        )
        image = self.request.query_params.get("image")

        if image:
            queryset = queryset.filter(image=image)

        return queryset

    def perform_create(self, serializer):

        image = serializer.validated_data["image"]

        if image.user != self.request.user:
            raise PermissionDenied(
                "Not allowed."
            )
        serializer.save()
        
class PolygonDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PolygonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Polygon.objects.filter(
            image__user=self.request.user
        )