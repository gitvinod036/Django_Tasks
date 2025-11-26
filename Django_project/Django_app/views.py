from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cloudinary
from .models import UserDetails
from .serializer import UserDetails_Serializers
import json
import bcrypt
import jwt,datetime
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.core.exceptions import ObjectDoesNotExist
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
      key="my_cookie",
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