from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Task.objects.filter(user=self.request.user)

        date = self.request.query_params.get("date")

        if date:

            queryset = queryset.filter(due_date=date)

        return queryset

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Task.objects.filter(user=self.request.user)