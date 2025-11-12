from django.db import models

# Create your models here.
class UserDetails(models.Model):
    id=models.BigAutoField(primary_key=True)
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=100,null=False,)
    email=models.EmailField(max_length=100,default="User@gmail.com")
    mobile=models.CharField(max_length=15)
    profile=models.URLField(default="empty")
