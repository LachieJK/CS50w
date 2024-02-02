from django.urls import path
from . import views

urlpatterns = [
    path("", views.open, name="open"),
    path("index", views.index, name="index"),
    path("checklist/<int:list_id>", views.checklist, name="checklist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete_list/<int:list_id>", views.delete_list, name="delete_list"),
    path("edit_list_name/<int:list_id>", views.edit_list_name, name="edit_list_name"),
    path("delete_task/<int:task_id>", views.delete_task, name="delete_task"),
    path("edit_task/<int:task_id>", views.edit_task, name="edit_task")
]