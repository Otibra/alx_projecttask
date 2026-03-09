# Import the Task and Project models from the current app
from .models import Task, Project

# Import Django REST Framework serializers
from rest_framework import serializers

# Serializer for the Project model
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project          # ✅ Specifies the model this serializer is for
        fields = '__all__'       # ✅ Include all fields from the Project model

# Serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for write operations
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),  # ensures the ID exists
        source='project',               # maps it to the model's project field
        write_only=True                 # only needed for input
    )
    
    # Keep nested project details for output
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority_level', 'status', 'project', 'project_id']
        