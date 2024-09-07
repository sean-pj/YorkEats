from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all, name="all"),
    path("later", views.later, name="later"),
    path("edit", views.edit, name="edit"),
    path("rating", views.rating, name="rating"),
    path("maps", views.maps, name="maps"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]