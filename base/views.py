from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task 

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.models import User


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name= 'base/register.html'
    form_class = UserCreationForm 
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


 
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        return context
    



class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDeleteView(LoginRequiredMixin, DeleteView):  # 🔁 Rename it
    model = Task 
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class ProfilePage(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username']
    template_name = 'base/profile.html'
    success_url = reverse_lazy('tasks')

    def get_object(self):
        return self.request.user  # Only lets them edit their own profile 