from .views import *
from django.urls import path

urlpatterns = [
    path("", indexView, name="index"),
    path("login", loginView, name="login"),
    path("newTask", newTask, name="newTask"),
    path("logout", logoutView, name="logout"),
    path("register", registerView, name="register"),
    path("taskView/<str:name>", taskView, name="taskView"),
    path("deleteTask/<str:name>", deleteTask, name="deleteTask"),
    path("taskCompleted/<str:name>", taskCompleted, name="taskCompleted"),
    path("taskNotCompleted/<str:name>", taskNotCompleted, name="taskNotCompleted")
]
