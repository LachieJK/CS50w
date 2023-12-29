from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # Home page URL
    path("", views.open, name="open"),
    # Index page URL showing all posts
    path("index", views.index, name="index"),
    # Profile page URL for a specific user
    path("profile/<int:user_id>", views.profile, name="profile"),
    # URL for editing a user's profile
    path("edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),
    # URL to view posts from followed users
    path("following", views.following, name="following"),
    # URL for login functionality
    path("login", views.login_view, name="login"),
    # URL for logout functionality
    path("logout", views.logout_view, name="logout"),
    # URL for registration functionality
    path("register", views.register, name="register"),
    # URL for deleting a post
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),

    # API Routes
    # URL for editing a post
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    # URL for following or unfollowing a user
    path("follow/<int:profile_user_id>", views.follow, name="follow"),
    # URL for liking or unliking a post
    path("likes/<int:post_id>", views.likes, name="likes")
]

# Add a URL pattern to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
