from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from Login.models import Register, Login_Session
from django.utils import timezone
import traceback

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        status = ''
        print(request.user.__dict__,"login redirect url")

        full_name = str(request.user.first_name) + str(request.user.last_name)

        sign_obj,sign_created=Register.objects.get_or_create(Full_Name=full_name,Email = request.user.email)


        if sign_created==False:
            status = "User Already Exists"
        else:            
            status = "Registered Successfully"


        login_session_obj = Login_Session.objects.filter(Email = request.user.email ,User_Id = sign_obj,Logged_out__isnull=True)

        print(login_session_obj.count())

        if login_session_obj.count() == 0:

            login_session_obj = Login_Session.objects.create(Email = request.user.email ,User_Id = sign_obj)
                

        print(status)

        request.session['user_mode'] = 'google'
        request.session['full_name'] = full_name
        request.session['email'] = request.user.email



        path = "/login"
        return path




    def get_logout_redirect_url(self, request):

        status = ''
        try:
            full_name = str(request.user.first_name) + str(request.user.last_name)

            sign_obj,sign_created=Register.objects.get_or_create(Full_Name=full_name,Email = request.user.email)

            if sign_created==False:
                status = "Logged out success"

                login_session_obj = Login_Session.objects.filter(User_Id = sign_obj,Logged_out=None)[0]
                login_session_obj.Logged_out = timezone.now()
                login_session_obj.save()


            else:            
                status = "Log out issue"
        except Exception as e:
            traceback.print_exc()
            
        

        print(status)


        path = "/index"
        return path
        