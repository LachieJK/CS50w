from django.contrib import admin
from checklist.models import User, List, Task

# Register your models here.
admin.site.register(User)
admin.site.register(List)
admin.site.register(Task)