from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cloudinary
from .models import UserDetails
from .serializer import UserDetails_Serializers
import json
import bcrypt
import jwt,datetime
# Create your views here.

def Welcome(req):
    return HttpResponse("Welcome")

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
        return HttpResponse("New user Registered Successfully")
      except Exception as e:
         return HttpResponse(f"Error {e}")
           
    else:
        return HttpResponse("Invalid method")


def login(req):
   user_data=json.loads(req.body)
   check_user=UserDetails.objects.get(username=user_data["name"])   #we get objects need to convert them json to string
   serialized=UserDetails_Serializers(check_user)
  #  print(user_data,serialized.data)
   
   encrypted_password=serialized.data["password"]
   user_password=user_data["password"]
   is_true=bcrypt.checkpw(user_password.encode("utf-8"),encrypted_password.encode("utf-8"))  #we cannot come to strings so we convert them to bytes and perform 
   
   user_payload={
      "name":serialized.data["username"],
      "email":serialized.data["email"],
      # "iat":datetime.datetime.now()+datetime.timedelta(seconds=30)
   }
   token=jwt.encode(payload=user_payload,key="django-insecure-&kvlv)8m=p=qc+82l^kvd-89uz(z=8_2wrdliq%-q&c(j#uybu",algorithm="HS256")
   print(token)
   Data=jwt.decode(jwt=token,key="django-insecure-&kvlv)8m=p=qc+82l^kvd-89uz(z=8_2wrdliq%-q&c(j#uybu",algorithm="HS256")
   print(Data)


   if is_true:
      return HttpResponse(f"{user_data['name']}  Welcome to the app")
   else:
      return HttpResponse("Try again Untill you Login")
  #  encrypted=serialized.data["password"]
  #  print(user_data,encrypted)


@csrf_exempt
def delete(req,id):
   if req.method=="DELETE" and id :
       get_user=UserDetails.objects.get(id=id)
       get_user.delete()
       return HttpResponse(f"{get_user['username']}User Deleted Sucessfully")
   else:
      raise TypeError("Invalid Method or Enter Id")