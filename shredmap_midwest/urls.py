from django.urls import path
from shredmap_midwest import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:resort_id>", views.resort_view, name="resort_view"),
    path("resorts", views.resorts, name="resorts"),
    path("howto", views.how_to, name="how_to"),

    # API Routes
    path("resort/<int:resort_id>", views.resort, name="resort"),
    path("all-resorts", views.all_resorts, name="all_resorts"),
    path("user_visited", views.user_visited, name="user_visited"),
]
