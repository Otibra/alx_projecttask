from rest_framework import serializers
from .models import Task, Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    # Make project_id optional
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True,
        required=False,   # ✅ optional now
        allow_null=True   # ✅ allows null values
    )

    # Nested project details for output
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 
            'priority_level', 'status', 'project', 'project_id'
        ]
        