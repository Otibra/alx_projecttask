from rest_framework import generics, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

# Base view to apply authentication and user filtering
class TaskBaseView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

# List + Create
class TaskListCreateView(TaskBaseView, generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'title', 'priority']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve / Update / Delete
class TaskDetailView(TaskBaseView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

