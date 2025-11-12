from django.urls import path
from . import views


urlpatterns=[
    path("Welcome/",view=views.Welcome),
    path("register/",view=views.register),
    path("login/",view=views.login),
    path("delete/<int:id>",view=views.delete)
]