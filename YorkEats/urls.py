from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all, name="all"),
    path("edit", views.edit, name="edit"),
    path("rating", views.rating, name="rating"),
    path("public_rating/<int:id>", views.public_rating, name="public_rating"),
    path("user_rating/<int:id>", views.user_rating, name="user_rating" ),
    path("maps", views.maps, name="maps"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]