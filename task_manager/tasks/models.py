from django.db import models
from django.contrib.auth.models import User  # Import User model

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    completed = models.BooleanField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    photo1 = models.ImageField(blank=True, null=True)
    photo2 = models.ImageField(blank=True, null=True)
    photo3 = models.ImageField(blank=True, null=True)

    
    username = models.ForeignKey(User, on_delete=models.CASCADE)  # Use ForeignKey to User model

    def __str__(self):
        return self.title
