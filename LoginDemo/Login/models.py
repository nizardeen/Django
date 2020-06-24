from django.db import models
import uuid
from django.utils import timezone


class Register(models.Model):
    Full_Name = models.CharField(max_length = 100,blank=True, null=True)
    Password = models.CharField(max_length = 256,null=True,blank=True)
    Mobile = models.BigIntegerField(unique=True,null=True,blank=False)
    Passport_No = models.CharField(max_length = 100,blank=True, null=True)
    DOB = models.CharField(max_length = 100,blank=True, null=True)
    Age = models.IntegerField(null=True,blank=True)
    Email = models.EmailField(blank=True, null=True)
    Image = models.FileField(null = True ,blank = True)


class Login_Session(models.Model):
    User_Id = models.ForeignKey(Register,on_delete=models.CASCADE)
    Email = models.EmailField(blank=True, null=True)
    Logged_in = models.DateTimeField(default=timezone.now,blank=True,null=True)
    Logged_out = models.DateTimeField(null=True,blank=True)
        
