from django.contrib import admin
from .models import Task

# Register your models here.
class AdminTast(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'priority', 'completed', 'creation_date', 'last_update', 'photo1','photo2','photo2', 'username')
admin.site.register(Task,AdminTast)


