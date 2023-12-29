from django.contrib import admin
from network.models import User, Profile, Following, Post

# All of my models registered for the Django Admin Interface
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Post)