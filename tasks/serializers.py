from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 🔹 Prevents manual modification

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'completed', 'created_at']
        read_only_fields = ['user']  # 🔹 Ensures 'user' cannot be modified manually

    def create(self, validated_data):
        """
        Assigns the task to the authenticated user automatically.
        """
        validated_data['user'] = self.context['request'].user  # 🔹 Assign the logged-in user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
