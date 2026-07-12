from django.urls import path

from .views import (
    ImageListCreateView,
    ImageDetailView,
    PolygonListCreateView,
    PolygonDetailView,
)

urlpatterns = [

    path(
        "images/",
        ImageListCreateView.as_view(),
    ),

    path(
        "images/<int:pk>/",
        ImageDetailView.as_view(),
    ),

    path(
        "polygons/",
        PolygonListCreateView.as_view(),
    ),

    path(
        "polygons/<int:pk>/",
        PolygonDetailView.as_view(),
    ),

]