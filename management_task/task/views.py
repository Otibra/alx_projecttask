from rest_framework import generics, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer
from rest_framework.exceptions import PermissionDenied



# Base view that applies authentication and filters tasks by the logged-in user
class TaskBaseView(generics.GenericAPIView):

    # Require token authentication for all requests
    authentication_classes = [TokenAuthentication]

    # Only authenticated users can access these views
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only tasks that belong to projects owned by the logged-in user
        # Relationship: Task → Project → User
        return Task.objects.filter(project__user=self.request.user)


# View for listing all tasks and creating a new task
class TaskListCreateView(TaskBaseView, generics.ListCreateAPIView):

    # Serializer used to convert Task model data to JSON and validate input
    serializer_class = TaskSerializer

    # Enable ordering and searching in the API
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    # Fields that can be used for ordering results
    ordering_fields = ['created_at', 'title', 'priority_level']

    # Fields that can be searched using the search query parameter
    search_fields = ['title', 'description']

    # Default ordering (latest tasks first)
    ordering = ['-created_at']

    
    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')

        # Ensure the project belongs to the authenticated user
        if project.user != self.request.user:
            raise PermissionDenied("You cannot create tasks in another user's project")

        serializer.save()


# View for retrieving, updating, or deleting a specific task
class TaskDetailView(TaskBaseView, generics.RetrieveUpdateDestroyAPIView):

    # Serializer used for task data
    serializer_class = TaskSerializer
