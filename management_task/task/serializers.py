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
    # Nest the ProjectSerializer to show project details in the Task output
    project = ProjectSerializer(read_only=True)  # ✅ read_only prevents editing via this serializer

    class Meta:
        model = Task             # ✅ Specifies the model this serializer is for
        fields = '__all__'       # ✅ Include all fields from the Task model
