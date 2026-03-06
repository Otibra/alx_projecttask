from rest_framework import generics, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer

# Base view to apply authentication and user filtering
class TaskBaseView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only tasks belonging to the requesting user are returned
        return Task.objects.filter(user=self.request.user)

# List + Create tasks
class TaskListCreateView(TaskBaseView, generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'title', 'priority']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Automatically set the user of the task to the authenticated user
        serializer.save(user=self.request.user)

# Retrieve / Update / Delete tasks
class TaskDetailView(TaskBaseView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
