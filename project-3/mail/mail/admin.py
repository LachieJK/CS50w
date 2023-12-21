from django.contrib import admin
from .models import User, Email

# All of my models registered for the Django Admin Interface
admin.site.register(User)
admin.site.register(Email)