from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task
from .forms import  TaskForm, Task_edit
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def start(request):
    return render(request,'start.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,username=email, password=password)
        if user is  not None:
            login(request, user)
            return redirect('task_list')
    return render(request,'login.html')


def user_signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

        # Create new user
        try:
            user = User.objects.create_user(username=email, password=password)
            user.first_name = name  # Store the user's name
            user.save()
            messages.success(request, "Sign up successful! You can now log in.")
            return redirect('login')  # Redirect to login page after successful signup
        except Exception as e:
            messages.error(request, f"Error during signup: {str(e)}")

    return render(request, 'signup.html') 
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # Fetch tasks for the logged-in user
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')  # Get the page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the tasks for the current page

    # Pass the paginated tasks to the template
    return render(request, 'task_list.html', {'tasks': page_obj})


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Fetch the task by ID and user
    if request.method == "POST":
        form = Task_edit(request.POST, instance=task)  # Bind the form to the task instance
        if form.is_valid():
            form.save()  # Save the updated task
            messages.success(request, "Task updated successfully.")
            return redirect('task_list')  # Redirect to the task list view
    else:
        form = Task_edit(instance=task)  # Pre-fill the form with the existing task data

    return render(request, 'edit.html', {'form': form, 'task': task})  # Render the form

# Delete Task View
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Fetch the task by ID and user
    if request.method == "POST":
        task.delete()  # Delete the task
        messages.success(request, "Task deleted successfully.")
        return redirect('task_list')  # Redirect to the task list view

    return render(request, 'delete.html', {'task': task}) 

@login_required
def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user to the task
            task.save()  # Save the task to the database
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')  # Redirect to the task list page
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})
