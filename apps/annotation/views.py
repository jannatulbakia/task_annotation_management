import mimetypes

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponseRedirect

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

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


class ImageFileView(APIView):
    """Stream the raw image file for an uploaded image (authenticated)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            image_obj = UploadedImage.objects.get(pk=pk, user=request.user)
        except UploadedImage.DoesNotExist as exc:
            raise Http404("Image not found.") from exc

        if not image_obj.image:
            raise Http404("Image file not found.")

        image_url = image_obj.image.url
        if image_url.startswith(("http://", "https://")):
            return HttpResponseRedirect(image_url)

        try:
            file_handle = image_obj.image.open("rb")
        except FileNotFoundError as exc:
            raise Http404("Image file missing on server.") from exc

        content_type, _ = mimetypes.guess_type(image_obj.image.name)
        return FileResponse(
            file_handle,
            content_type=content_type or "application/octet-stream",
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
            raise PermissionDenied("Not allowed.")

        serializer.save()


class PolygonDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PolygonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Polygon.objects.filter(
            image__user=self.request.user
        )


class DebugStorageView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "STORAGES": settings.STORAGES,
        })