from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_huddle_ready_email
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer, UserResponseSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt_token(user):
    """Generates a JWT token for the provided user."""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expiration (24 hours)
        'iat': datetime.utcnow(),  # Issued at time
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

class SendEmailView(APIView):
    """Create a user and send an email with a link that includes a JWT token."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(email=email, password=None)

            token = generate_jwt_token(user)

            app_link = f"https://yourapp.com/auth?token={token}"

            send_huddle_ready_email(email, app_link)

            return Response({"message": "User created and email with link sent."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        
