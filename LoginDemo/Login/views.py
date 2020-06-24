from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from datetime import date , datetime ,timedelta
from django.utils import timezone
from functools import wraps
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from dateutil.relativedelta import relativedelta
import traceback
import  hashlib
import base64

from django.contrib.auth import logout


from .models import Register,Login_Session



@csrf_exempt
def index(request):
    return render(request, "index.html",{})


@csrf_exempt
def register(request):
    status = ""
    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        Full_Name = requestData.get('FullName',None)
        Password =requestData.get('Password',None)
        Mobile = requestData.get('Mobile',None)
        Passport_No =requestData.get('PassportNo',None)
        DOB = requestData.get('DOB',None)
        Age = requestData.get('Age',None)
        Email = requestData.get('Email',None)


        if len(request.FILES) != 0:
            Image=request.FILES['Image']
        else:
            Image =""


        #hashing  password
        hashed_password = hash_password(Password)

        #create user data
        sign_obj,sign_created=Register.objects.get_or_create(Full_Name=Full_Name,Mobile=Mobile,Email=Email,Passport_No=Passport_No,Password=hashed_password,
            DOB=DOB,Age=Age,Image = Image)

        if sign_created==False:
            status = "Data Already Exits"
        else:            
            status = "Registered Successfully"

        return render(request,"index.html",{'check_Login':status})

    except Exception as e:
        traceback.print_exc()
        status = "Check the Inputs"

    return JsonResponse({"status":status},status=200)



def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
    



@csrf_exempt
def login(request):
    status = ""
    Mobile = ""
    user_obj = None
    login_session_obj = None
    login_lists = None

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    print(request.method)
    print(requestData)
    try:

        if request.method == 'POST':

            encoded_data = requestData.get('encoded_data',None)
            print(encoded_data)
            base64_bytes = encoded_data.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            print(message)

            UserName = message.split(':/:')[0].strip()
            Password = message.split(':/:')[1].strip()

            print(UserName,Password)

            try:
            
                #get user obj
                user_obj = Register.objects.get(Email = UserName)
               
                hashed_password = user_obj.Password

                #check password
                if check_password(hashed_password, Password):

                    request.session['user_mode'] = 'registered'

                    login_session_obj = Login_Session.objects.filter(User_Id = user_obj)

                    login_sessions = login_session_obj.filter(Logged_out__isnull=True)


                    if login_sessions.count() == 0:

                        login_create_session = Login_Session.objects.create(Email = user_obj.Email ,User_Id = user_obj)


                    login_session_obj = login_session_obj.filter(Logged_out__isnull = False)
                    login_lists = list(login_session_obj.values())

                    request.session['full_name'] = user_obj.Full_Name
                    request.session['email'] = user_obj.Email

                    status = "success"

                else :
                    status = "Invaild Password"

            except Exception as e:
                traceback.print_exc()
                status = "Invalid Email Id"


            return JsonResponse({"status":status,'login_data':login_lists},status=200)


        elif request.method == 'GET':
            print('logged in success')

            full_name = request.session['full_name']
            email = request.session['email']

            login_session_obj = Login_Session.objects.filter(User_Id__Full_Name = full_name,User_Id__Email = email,Logged_out__isnull = False)
            login_lists = list(login_session_obj.values())

            status = 'success'

    except Exception as e:
        status = "User Not Found"
        traceback.print_exc()


    if status=="success":

        return render(request,"dashboard.html",{'login_data':login_lists})

    else:
        return render(request,"index.html",{'check_Login':status})



@csrf_exempt
def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()




@csrf_exempt
def user_logout(request):

    print(request.method)
    
    try:

        full_name = request.session['full_name']
        email = request.session['email']

        print(full_name,email)

        sign_obj=Register.objects.get(Full_Name=full_name,Email = email)

        status = "Logged out success"

        login_session_obj = Login_Session.objects.filter(User_Id = sign_obj,Logged_out=None)[0]
        login_session_obj.Logged_out = timezone.now()
        login_session_obj.save()
        
        request.session['full_name'] = ''
        request.session['email'] = ''

        logout(request)

    except Exception as e:
        traceback.print_exc()

    return render(request,"index.html",{})



@csrf_exempt
def updatePassword(request):
    status = ""
    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        Email = request.session['email']
        OldPassword = requestData.get('OldPassword',None)
        NewPassword = requestData.get('NewPassword',None)

        print(OldPassword,NewPassword)
        
        User_obj = Register.objects.get(Email = Email)

        if check_password(User_obj.Password, OldPassword):
            
            hashed_password = hash_password(NewPassword)

            User_obj.Password = hashed_password
            
            User_obj.save()
            
            status = "Password Reset Successfully"

        else:
            status = "Wrong Password"

        
    except Exception as e:
        status = "User not found"
        traceback.print_exc()

    return JsonResponse({"status":status},status=200)