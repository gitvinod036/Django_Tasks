from django.urls import path
from . import views


urlpatterns=[
    path("Welcome/",view=views.Welcome),
    path("register/",view=views.register),
    path("login/",view=views.login),
    path("delete/<int:id>",view=views.delete),
    path("get_user/<int:id>",view=views.get_user),
    path("get_user/",view=views.get_user),
    path("send_file/",view=views.send_file)
]