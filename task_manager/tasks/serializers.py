from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Task

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class TaskSerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(choices=PRIORITY_CHOICES)
    photo1 = serializers.ImageField(max_length=None, allow_empty_file=True, required=False)  # Add this line
    photo2 = serializers.ImageField(max_length=None, allow_empty_file=True, required=False)  # Add this line
    photo3 = serializers.ImageField(max_length=None, allow_empty_file=True, required=False)  # Add this line
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'completed', 'creation_date', 'last_update', 'photo1', 'photo2', 'photo3', 'username']

       
        read_only_fields = ('creation_date', 'last_update')
        