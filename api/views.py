from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_huddle_ready_email
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer, UserResponseSerializer

class SendEmailView(APIView):
    """_summary_

    Endpoint: POST /api/send-email/
    Functionality: Collects the user's email, then sends a background email using Celery with a 
                    customizable message.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if email:
            # Call celery task
            # send_huddle_ready_email.delay(email)
            send_huddle_ready_email(email)
            return Response({"message": "Email will be sent shortly."}, status=status.HTTP_200_OK)
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)


class TaskCreateView(generics.CreateAPIView):
    """_summary_

    Endpoint: Create a new task (POST /api/tasks/)
    """
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskListView(generics.ListAPIView):
    """_summary_

    Endpoint: Retrieve all tasks (GET /api/tasks/)
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDetailView(generics.RetrieveAPIView):
    """_summary_

    Endpoint 3: Retrieve a specific task (GET /api/tasks/<id>/)
    """
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    

class UserResponseCreateView(generics.CreateAPIView):
    """
    Endpoint to collect user responses to the experience questions (POST /api/responses/)
    """
    serializer_class = UserResponseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        