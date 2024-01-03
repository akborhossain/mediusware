import django_filters
from django_filters import CharFilter,DateFilter
from .models import *
from django import forms

class TaskFilter(django_filters.FilterSet):
    title=CharFilter(field_name='title', lookup_expr='icontains')
    due_date = django_filters.DateFilter(
        field_name='due_date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    creation_date=  django_filters.DateFilter(
        field_name='creation_date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )  
    class Meta:
        model=Task
        fields=['title','priority','due_date','creation_date','completed']