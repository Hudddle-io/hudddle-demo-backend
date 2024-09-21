from rest_framework import serializers
from .models import Task, UserResponse

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['experience', 'huddle_feedback', 'feature_suggestion']