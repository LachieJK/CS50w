from django.contrib import admin
from .models import User, Category, Listings, Bids, Comments

# All of my models registered for the Django Admin Interface
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)