from datetime import timezone
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where email is the unique identifier for authentication.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Placeholder for permission check logic
        return True

    def has_module_perms(self, app_label):
        # Placeholder for module permissions logic
        return True

    def get_group_permissions(self, obj=None):
        # Placeholder for group permissions logic
        return set()

class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience = models.CharField(max_length=255)
    huddle_feedback = models.TextField()
    feature_suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response from {self.user.email}"

class Workroom(models.Model):
    workroom_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workrooms')
    members = models.ManyToManyField(User, related_name='workrooms', blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.workroom_name
    
    def add_member(self, user):
        """
        Adds a member to the workroom.
        """
        self.members.add(user)
        self.save()

    def remove_member(self, user):
        """
        Removes a member from the workroom.
        """
        self.members.remove(user)
        self.save()

    def get_members(self):
        """
        Returns a list of members in the workroom.
        """
        return self.members.all()
    
    def total_number_of_room_members(self):
        return self.members.count()

    def total_number_of_active_room_members(self):
        return self.members.filter(is_active=True).count()

    def total_number_of_non_active_room_members(self):
        return self.members.filter(is_active=False).count()
    

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    due_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=50, blank=True, null=True)
    tool = models.CharField(max_length=50, blank=True, null=True)
    recurring = models.BooleanField(default=False)
    duration = models.IntegerField(blank=True, null=True)
    estimated_time_for_completion = models.IntegerField(blank=True, null=True)
    workroom = models.ForeignKey(Workroom, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def start_timer(self):
        self.start_time = timezone.now()
        self.save()

    def stop_timer(self):
        self.end_time = timezone.now()
        self.save()

    def get_time_spent(self):
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60  # returns time in minutes
        return None

    def is_overdue(self):
        if self.get_time_spent() and self.estimated_time_for_completion:
            return self.get_time_spent() > self.estimated_time_for_completion
        return False
