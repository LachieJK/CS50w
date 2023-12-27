from django.contrib import admin
from network.models import User, Profile, Following, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Post)