from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task          # ✅ the model this serializer is for
        fields = '__all__' 
        
