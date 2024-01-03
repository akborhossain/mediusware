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

    class Meta:
        model = Task
        fields = '__all__'  # Serialize all fields of the Task model
        read_only_fields = ('creation_date', 'last_update')