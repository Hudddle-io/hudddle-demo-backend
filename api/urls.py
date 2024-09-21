from django.urls import path
from .views import (SendEmailView, TaskCreateView, TaskListView, TaskDetailView, UserResponseCreateView)

urlpatterns = [
    path('send-email/', SendEmailView.as_view(), name='send-email'),
    path('tasks/', TaskListView.as_view(), name='task-list'),  
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('responses/', UserResponseCreateView.as_view(), name='user-response-create'),
]