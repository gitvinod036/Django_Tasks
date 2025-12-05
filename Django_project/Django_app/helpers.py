#helpers function
from django.http import HttpResponse

def sample_decorator(func):
    def wrapper(request,*args,**kwargs):
        print(dir(request),"from req")
        print("Before Function ")
        new_fun=func(request,*args,**kwargs)
        return new_fun
    
    return wrapper 


def Another_decorator(func):
    print("before ")
    def wrapper(request,*args,**kwargs):
       if request.COOKIES.get('first_cookie'):
           return func(request)
       else:
           HttpResponse("Cookie needed")
    return wrapper