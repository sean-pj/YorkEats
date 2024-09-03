from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit", views.edit, name="edit"),
    path("rating", views.rating, name="rating"),
    path("rating/<int:id>", views.place_rating, name="place_rating"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]