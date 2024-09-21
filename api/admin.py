from django.contrib import admin
from .models import User, Workroom, Task, UserResponse

# Register your models here.
admin.site.register(User)
admin.site.register(Workroom)
admin.site.register(Task)
admin.site.register(UserResponse)