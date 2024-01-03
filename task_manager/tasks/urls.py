
from django.urls import re_path
from django.views.generic import TemplateView
from django.urls import path
from .views import CreateTaskView, TaskListView, TaskDeletionView,TaskCompleted ,TaskCreatAPI,TaskRetriveUD,TaskUpdateView, TaskDetailsView,LoginView,LogoutView,TaskAPI,SearchView,Registration


urlpatterns = [
    path('',LoginView.as_view(),name='user_login'),
    path('register/',Registration.as_view(),name='register'),
    path('tc/', CreateTaskView.as_view(), name='create_task'),
    path('tl/', TaskListView.as_view(), name='task_list'),
    path('td/<int:id>', TaskDeletionView.as_view(), name='task_deletion'),
    path('tu/<int:id>/', TaskUpdateView.as_view(), name='task_update'),
    path('tdts/<int:id>/', TaskDetailsView.as_view(), name='task_details'),
    path('tapi/',TaskAPI.as_view(),name='tapi'),
    path('tapi/<int:pk>/',TaskAPI.as_view(),name='tapi'),
    path('logout/',LogoutView.as_view(),name='user_logout'),
    path('search/',SearchView.as_view(),name='search'),
    path('complete/<int:id>/',TaskCompleted.as_view(),name='complete'),
    path('taskapi/', TaskCreatAPI.as_view(), name='taskapi'),
    path('taskapi/<int:pk>/',TaskRetriveUD.as_view()),
]
