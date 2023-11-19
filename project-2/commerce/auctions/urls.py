from django.urls import path

from . import views

urlpatterns = [
    path("", views.open, name="open"),
    path("index", views.index, name="index"),
    path("create", views.create, name="create"),
    path("category/<int:category_id>/", views.category, name="category"),
    path("error/<str:message>", views.error, name="error"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("watchlist/<int:user_id>/", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
