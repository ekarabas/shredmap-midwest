from nturl2path import url2pathname
from unicodedata import name
from django.urls import path
from shredmap_midwest import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:resort_id>", views.resort_view, name="resort_view"),
    path("test", views.test, name="test"),

    # API Routes
    path("resort/<int:resort_id>", views.resort, name="resort"),
    path("all-resorts", views.all_resorts, name="all_resorts"),
    path("user_visited", views.user_visited, name="user_visited"),
]
