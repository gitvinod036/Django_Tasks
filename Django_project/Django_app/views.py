from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cloudinary
from Django_app.models import DjangoAppUserdetails,Employee
from .serializer import UserDetails_Serializers
import json
import bcrypt
import jwt,datetime
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max,Min,Avg,Sum,Count

#CBV
# from django.view import View
from django.views.generic import View,ListView,DetailView,DeleteView,CreateView,UpdateView
from django.urls import reverse_lazy
from .forms.emp_form import EmpForm
# from ..forms.emp_form import EmpForm


from django.core.paginator import Paginator


# Create your views here.
from .helpers import Another_decorator,sample_decorator


# @sample_decorator
def welcome(req):
   res=HttpResponse("Welcome to Django App")
   res.set_cookie(
      key='first_cookie',
      value='Sample_cookie',
      max_age=60
   )
   return res
   print("from view")
   return HttpResponse("Welcome")




# @Another_decorator
# def sample(req):
#    print(req.COOKIES.get("first_cookie"), "From View")
#    return JsonResponse({"msg":"Welcome app"})

@csrf_exempt
def register(req):
    if req.method=="POST":
      try:
        id=req.POST.get("id")
        username=req.POST.get("name")
        password=req.POST.get("password")
        email=req.POST.get("email")
        mobile=req.POST.get("mobile")
        img_url=req.FILES.get("profile")
        img_url=cloudinary.uploader.upload(img_url)

        user_password=password.encode("utf-8")
        u_salt=bcrypt.gensalt(12)
        encrypted_password=bcrypt.hashpw(password=user_password,salt=u_salt)
        encrypted_password=encrypted_password.decode("utf-8")

        created_user=UserDetails.objects.create(id=id,username=username,password=encrypted_password,email=email,mobile=mobile,profile=img_url["secure_url"])
      #   new_user=UserDetails.objects.get(id=created_user.id)
      #   new_user=UserDetails_Serializers(new_user)
        send_mail(subject="Welcome to Our App! 🎉",   
                  message=f'''Hi {username},
Welcome to our application! Your registration was successful, and we're excited to have you on board.
Feel free to explore and enjoy all the features we’ve built for you.''',recipient_list=[email],from_email=settings.EMAIL_HOST_USER)
        return JsonResponse({"New User":"Successfull"})
      except Exception as e:
         return HttpResponse(f"Error {e}")
    else:
        return HttpResponse("Invalid method")

@csrf_exempt
def login(req):
   user_data=json.loads(req.body)
   try:
    check_user = UserDetails.objects.get(username=user_data["name"])
   except ObjectDoesNotExist:
    return HttpResponse("User does not exist", status=400)
   # check_user=UserDetails.objects.get(username=user_data["name"])   
   serialized=UserDetails_Serializers(check_user)
   print(user_data,serialized.data)
   
   encrypted_password=serialized.data["password"]
   user_password=user_data["password"]
   is_true=bcrypt.checkpw(user_password.encode("utf-8"),encrypted_password.encode("utf-8"))   
   print(is_true)
   if is_true==False:
      return HttpResponse("Invalid Cerdentials Try Again")
   else:
    user_payload={
      "name":serialized.data["username"],
      "email":serialized.data["email"],
      "iat":datetime.datetime.now(),
      "exp":datetime.datetime.now()+datetime.timedelta(seconds=360)
    }

    token=jwt.encode(payload=user_payload,key="django-insecure-&kvlv)8m=p=qc+82l^kvd-89uz(z=8_2wrdliq%-q&c(j#uybu",algorithm="HS256")
    print(token)
   

    res=HttpResponse("Cookie is set and successfully registered")
   
    res.set_cookie(
      key="first_cookie",
      value=token,
      httponly=True,
      max_age=1800
    )
   return res


def get_user(req,id=None):
   if req.method=="GET":
      if id:
         get_user=UserDetails.objects.get(id=id)
         userdata=UserDetails_Serializers(get_user)
         return JsonResponse({"userdata":userdata.data})
      else:
         users_data=UserDetails.objects.all()
         all_user_data=UserDetails_Serializers(users_data,many=True)
         return JsonResponse({"Users_details":all_user_data.data})
   else:
      return HttpResponse("Invalid menthod to get users")









   # Decoded_Data=jwt.decode(jwt=token,key="django-insecure-&kvlv)8m=p=qc+82l^kvd-89uz(z=8_2wrdliq%-q&c(j#uybu",algorithms="HS256")
   # print(Decoded_Data)


   # if is_true:
   #    return HttpResponse(f"{user_data['name']} Your Token is :{token} And the Decode Data is :  Welcome to the app")
   # else:
   #    return HttpResponse("Try again Untill you Login")
  #  encrypted=serialized.data["password"]
  #  print(user_data,encrypted)


@csrf_exempt
def delete(req,id):
   try:
    if req.method=="DELETE" and id :
       get_user=UserDetails.objects.get(id=id)
       get_user.delete()
       return HttpResponse(f"{get_user['username']}User Deleted Sucessfully")
    else:
       return HttpResponse("Invalid Method or ID")
   except Exception as e:
      return HttpResponse(f"The error is {e}")
   


@csrf_exempt 
def send_file(req):
   user_email=req.POST.get("email")
   pic=req.FILES.get("file")

   email=EmailMessage(subject="Sending Email",
                      body="Welcome To ",
                      from_email=settings.EMAIL_HOST_USER,
                      to=[user_email])
   email.attach_file("C://Users//S VINAY KUMAR//Pictures//img2.jpg")
   email.send()
   return HttpResponse("Message Send Successfully")


def is_valid_user(request):
   try:
      cookie_token=request.COOKIES.get("first_cookie")
      if not cookie_token:
         return False
      data=jwt.decode(jwt=cookie_token,key='django-insecure-&kvlv)8m=p=qc+82l^kvd-89uz(z=8_2wrdliq%-q&c(j#uybu',algorithms=["HS256"])
      return data    #return Decoded
   except Exception:
      return False
   




#TEmplates




@csrf_exempt
def start(request):
   name=request.POST.get("name")
   Email=request.POST.get("email")
   mobile=request.POST.get("mobile")
   age=request.POST.get("age")
   return render(request,"./basic.html", context={"value":name,"email":Email,"mobile":mobile,"age":age})


def show(req):
 return render(req,"./sample2.html")
    

def loops(req):
   names=["manoj","arvind","johhny","vinod","raju","dharma","surya","bala","Iphone"]
   return render(req,"./sample4.html" ,context={"names":names})



#ORM with Imported table
def emp_table(req):
   data=Employee.objects.all()
   # return HttpResponse(data)
   # data=list(data)
   for emp in data:
      print(emp.salary)
      # return HttpResponse(emp.name,emp.salary)
   count_emp=data.aggregate(Count('name'))
   max_salary=data.aggregate(Max('salary'))
   min_salary=data.aggregate(Min("salary"))
   avg_salary=data.aggregate(Avg('salary'))

   # return JsonResponse({"max":max_salary})
   return JsonResponse({"max":count_emp})


#Sql Injection :


#CBV

#BASIC VIEW
class Sample(View):
   def get(self,req):
      return HttpResponse("Sample View")
   

#LIST VIEW --from Generic 
class EmployeeList(ListView):
   model=Employee
   context_object_name="employee"
   template_name="emp_list.html"


class SingleView(DetailView):
   model=Employee
   context_object_name="employee"
   template_name="emp_details.html"

class DelEmp(DeleteView):
   model=Employee
   context_object_name="emp"
   template_name="delete_emp.html"
   success_url=reverse_lazy("emp_list")
   
class CreateEmp(CreateView):
   model=Employee
   form_class=EmpForm
   template_name="emp_reg.html"
   success_url=reverse_lazy("emp_list")


class UpdateEmp(UpdateView):
   model:Employee
   form_class=EmpForm
   template_name="emp_reg.html"
   success_url=reverse_lazy("emp_list")



def emp_pages(req):

   all_data=Employee.objects.all().values()
   item_count=req.GET.get("items")
   print(item_count)
   
   paginator=Paginator(all_data,item_count)   #Data,Items per page
   #Page number
   page_number=req.GET.get("page",1)  #  req of wanted page ...getting the current page from req
   # print(page_number)
   page_obj=paginator.get_page(page_number)  #to cheeck whether page exists if exists get page number from data
   print(page_obj)
    
   search=req.GET.get("prop")
   print(search)
   if search:
      all_data=all_data.filter(city__icontains=search)

   res_data={
      "current_page":page_obj.number,#indicates current page
      "page_size":paginator.per_page,  #records per page
      "total_pages":paginator.num_pages,  #  per page 5 total no of pages 
       "total_items":paginator.count,     #total no of items
       "has_next":page_obj.has_next(),
       "has_previous":page_obj.has_previous(),
       "next_page":page_obj.next_page_number() if page_obj.has_next() else None,
       "previous_page":page_obj.previous_page_number() if page_obj.has_previous() else None,
       "result":list(page_obj)

   }
   return JsonResponse({"data":res_data }) 