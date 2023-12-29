from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.open, name="open"),
    path("index", views.index, name="index"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),

    # API Routes
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("follow/<int:profile_user_id>", views.follow, name="follow"),
    path("likes/<int:post_id>", views.likes, name="likes")
]

# Add a URL pattern to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)