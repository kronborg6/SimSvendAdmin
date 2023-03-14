from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("users", views.users, name="users"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("matches", views.matches, name="matches"),
    path("tournements", views.tournements, name="tournements"),
    path("edit_role", views.edit_role, name="edit_role"),
    path("edit_tour", views.edit_tour, name="edit_tour")

]
