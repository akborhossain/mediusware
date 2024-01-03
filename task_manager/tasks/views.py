from django.shortcuts import render, redirect
from django.views import View
from .forms import TaskForm,UserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import get_object_or_404
from .models import User,Task
from .forms import LoginForm
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializer
from .filter import *
from rest_framework import status
class Registration(View):
    template_name='register.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('task_list')  
        form=UserCreateForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
        return render(request,self.template_name,{'form':form})

class CreateTaskView(View):
    template_name = 'create_task.html'

    @method_decorator(login_required(login_url='user_login'))
    def get(self, request):
        form = TaskForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)  # Create the task object but don't save it yet
            task.username = request.user  # Set the username field
            task.save()  # Now save the task with the username
            return redirect('task_list')  # Redirect to the task list view
        
        return render(request, self.template_name, {'form': form})
    
from django.core.paginator import Paginator

class TaskListView(View):
    template_name = 'task_list.html'

    @method_decorator(login_required(login_url='user_login'))
    def get(self, request):
        # Retrieve tasks for the currently logged-in user
        tasks_list = Task.objects.all().order_by('-creation_date')  # Ordering tasks by creation_date

        myFilter=TaskFilter(request.GET, queryset=tasks_list)
        tasks_list=myFilter.qs

        # Pagination setup
        paginator = Paginator(tasks_list, 10)  # Show 10 tasks per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'filter':myFilter
        }

        return render(request, self.template_name, context)


class TaskDetailsView(View):
    template_name = 'task_details.html'

    @method_decorator(login_required(login_url='user_login'))
    def get(self, request, id):
        try:
            task = get_object_or_404(Task, id=id)
            return render(request, self.template_name, {'task': task})
        except Http404:
            messages.error(request, 'Task not found.')
            # Handle the 404 case, maybe redirect or render a different template
            return redirect('task_list')  # or any other appropriate action

    @method_decorator(login_required(login_url='user_login'))
    def post(self, request, id):
        task = get_object_or_404(Task, id=id)

        if request.method == 'POST':
            # Handle the post request
            return redirect('task_details', id=id)



class TaskUpdateView(View):
    template_name = 'task_update.html'

    @method_decorator(login_required(login_url='user_login'))
    def get(self, request, id):
        if request.user.is_superuser:
            try:
                task = get_object_or_404(Task, id=id)
                form = TaskForm(instance=task)
                return render(request, self.template_name, {'form': form})
            except Http404:
                messages.error(request, 'Task not found.')
                # Handle the 404 case, maybe redirect or render a different template
                return redirect('task_list')  # or any other appropriate action
        else:
            return redirect('task_details', id=id)
        
    @method_decorator(login_required(login_url='user_login'))
    def post(self, request, id):
        try:
            task = get_object_or_404(Task, id=id)
            if request.user.is_superuser:
                if request.method == 'POST':
                    form = TaskForm(request.POST, request.FILES, instance=task)
                    if form.is_valid():
                        form.save()
                        return redirect('task_details', id=id)
            else:
                print('wrong')
                return redirect('task_details', id=id)
        except Http404:
            messages.error(request, 'Task not found.')
            # Handle the 404 case in post as well
            return redirect('task_list')  # or any other appropriate action

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

class TaskDeletionView(View):
    template_name = 'task_deletion.html'

    @method_decorator(login_required(login_url='user_login'))
    def get(self, request, *args, **kwargs):
        try:
            del_id = kwargs['id']
            task = get_object_or_404(Task, pk=del_id)
            return render(request, self.template_name, {'task': task})
        except Http404:
            messages.error(request, 'Task not found.')
            return render(request, self.template_name) 

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            del_id = kwargs['id']
            task = get_object_or_404(Task, pk=del_id)
            task.delete()
            # Send a success message
            messages.success(request, 'Task successfully deleted.')
            return redirect('task_deletion',id=del_id)  # Redirect to the task list or any other page
        else:
            # Send an error message if user is not a superuser
            messages.error(request, 'You do not have permission to delete tasks.')
            return redirect('task_list')  # Redirect to the task list or any other page

    
class TaskCompleted(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            id = kwargs['id']
            task=Task.objects.get(pk=id)
            if not task.completed:
                task.completed=True
                task.save()
                return redirect('task_details',id=id)
            else:
                messages.add_message(request, messages.WARNING, 'You already completed this task.')
                return redirect('task_details',id=id)
        else:
            return redirect('task_details',id=kwargs['id'])

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('task_list')  
        # Display the login form
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('task_list')  
        # Process the login form data
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a page after successful login
                return redirect('task_list')
            else:
                # Handle authentication failure
                return render(request, self.template_name, {'form': form, 'error': 'Invalid login credentials'})
        return render(request, self.template_name, {'form': form})
    

class LogoutView(View):

    @method_decorator(login_required(login_url='user_login'))
    def get(self, request):
        logout(request)
        return redirect('user_login')
    
class SearchView(View):
    template_name = 'task_list.html'

    @method_decorator(login_required(login_url='user_login'))
    def post(self, request):
        # Redirecting to the task list page if GET request
        return redirect('task_list')

    @method_decorator(login_required(login_url='user_login'))
    def get(self, request):
        # Retrieve tasks for the currently logged-in user based on the search title
        """title = request.POST.get('title')
        tasks_list = Task.objects.filter(title__icontains=title)"""
        tasks=Task.objects.all()
        myFilter=TaskFilter(request.GET, queryset=tasks)
        tasks_list=myFilter.qs
        # Setting up pagination
        paginator = Paginator(tasks_list, 10)  # Display 10 tasks per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'filter':myFilter}
        
        if tasks_list.exists():
            context['page_obj'] = page_obj
        else:
            context['message'] = "No tasks found matching the search criteria."
        
        return render(request, self.template_name, context)


def update(request, id):
    if request.method=='POST':
        ta=Task.objects.get(id=id, username=request.user)
        fm=TaskForm(request.POST,instance=ta)
        if fm.is_valid():
            fm.save()
    else:
        ta=Task.objects.get(id=id,username=request.user)
        fm=TaskForm(instance=ta)

    return render(request,'task_update.html', {'form':fm})

#class base CRUD API

from django.http import Http404
@method_decorator(login_required(login_url='user_login'), name='dispatch')
class TaskAPI(APIView):
    def get(self,request, pk=None, format=None):
        if request.user.is_authenticated:
            id=pk
            if id is not None:
                try:
                    t=Task.objects.get(id=id)
                    serializer=TaskSerializer(t)
                    return Response(serializer.data)
                except Task.DoesNotExist:
                    raise Http404("Task does not exist")
            t=Task.objects.all()
            serializer=TaskSerializer(t, many=True)
            return Response(serializer.data)
    
    def post(self, request, pk=None, format=None):

        if pk is not None:
            msg = {'error': 'Cannot specify a primary key when creating a new task.'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_superuser:
            try:
                serializer=TaskSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    msg={'msg':'Successfully inserted data'}
                    return Response(msg)
                return Response(serializer.errors)
            except Http404:
                messages.error(request, 'Task not found.')
                return render(request, self.template_name) 
        else:
            msg={'msg':'Only superuser can add task.'}
            return Response(msg)
        
    def put(self, request, pk, format=None):
        if request.user.is_superuser:
            try:
                id=pk
                t=Task.objects.get(id=id)
                serializer=TaskSerializer(t,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Full data updated'})
                return Response(serializer.errors)
            except Task.DoesNotExist:
                raise Http404("Task does not exist")
        else:
            msg={'msg':'Only superuser can fully update task.'}
            return Response(msg)
    def patch(self,request,pk, format=None):
        if request.user.is_authenticated:
            id=pk
            try:
                t=Task.objects.get(id=id)
                serializer=TaskSerializer(t,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Partially data updated.'})
                return Response(serializer.errors)
            except Task.DoesNotExist:
                raise Http404("Task does not exist")
        else:
            msg={'msg':'Only authentic user can update task.'}
            return Response(msg)
    def delete(self, request,pk, format=None):
        if request.user.is_superuser:
            try:
                id=pk
                t=Task.objects.get(id=id)
                t.delete()
                return Response({'msg':'Deleted data'})
            except Task.DoesNotExist:
                raise Http404("Task does not exist")
        else:
            msg={'msg':'Only superuser can delete task.'}
            return Response(msg)



@method_decorator(login_required(login_url='user_login'), name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@method_decorator(login_required(login_url='user_login'), name='dispatch')
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



