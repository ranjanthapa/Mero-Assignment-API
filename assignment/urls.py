from django.urls import path
from . import views

app_name = "assignment"

urlpatterns = [
    path("create-group", views.CreateGroupView.as_view()),
    path("groups", views.ListGroupView.as_view()),
    path("join-group", views.JoinGroupView.as_view()),
    path("group/<slug:slug>/tasks", views.TaskView.as_view(), name="group_task"),
]