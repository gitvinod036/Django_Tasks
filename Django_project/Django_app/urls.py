from django.urls import path
from . import views
from django.views import View

from .views import Sample,EmployeeList,SingleView,DelEmp,CreateEmp,UpdateEmp

urlpatterns=[
    # path("Welcome/",view=views.Welcome),
    path("register/",view=views.register),
    path("login/",view=views.login),
    path("delete/<int:id>",view=views.delete),
    path("get_user/<int:id>",view=views.get_user),
    path("get_user/",view=views.get_user),
    path("send_file/",view=views.send_file),
    path("welcome/",view=views.welcome),
    # path("sample/",view=views.sample),
    path("is_valid_user/",view=views.is_valid_user),
    path("start/",view=views.start),
    path("show/",view=views.show,name="show"),
    path("loops/",view=views.loops,name="sample4"),
    path("emp_table/",view=views.emp_table),

    #CBV
    path("sample/",view=Sample.as_view()),
    path("emp_list/",view=EmployeeList.as_view()),
    path("emp/<int:pk>/",view=SingleView.as_view(),name="emp_details"),
    path("del_emp/<int:pk>/",view=DelEmp.as_view(),name="delete_emp"),
    path("reg_emp/",view=views.CreateEmp.as_view(),name="reg_emp"),
    path("update_emp/<int:pk>/",view=UpdateEmp.as_view(),name="update_emp"),




    path("emp_pages/",view=views.emp_pages)
] 