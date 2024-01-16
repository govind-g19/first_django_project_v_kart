from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout as vkart_loogout
# active user
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
#getting tokens 
from .utils import TokenGenerator,generate_token
# to redirect to specifice page after login
from django.contrib.auth.forms import AuthenticationForm

#sending mails
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import send_mass_mail, BadHeaderError
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage
# for class based view
from django.views.generic import View
# password generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#otp
from random import randint
# threding to reduce time

import threading

from django.urls import reverse
class  EmailThread(threading.Thread):
   
   def __init__(self,email_message):
      self.email_message=email_message
      threading.Thread.__init__(self)
   def run(self):
      self.email_message.send()

# Create your views here.
def signup(request):
    if request.method == "POST":
        # Retrieve form data from POST request
        uname            = request.POST.get('username')
        email            = request.POST.get('email')
        first_name       = request.POST.get('first_name')
        last_name        = request.POST.get('last_name')
        password         = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')

        # Ensure passwords match
        if password!= confirm_password:
            messages.warning(request, "Passwords do not match.")
            return render(request, 'auth/signup.html')

        # Check if username or email already exists in the database
        try:
          if User.objects.filter(username=uname).exists():
            messages.warning(request, "Username is taken.")
            return render(request, 'auth/signup.html')
        except Exception:
          pass

        # Create a new User object
        user = User.objects.create_user(
            username  = uname,
            email      = email,
            first_name = first_name,
            last_name  = last_name,
            password   = password,
        )

        # Save the user to the database
        user.is_active= False
        user.save()
        current_site= get_current_site(request)
        email_subject =" Ativate Your Account "
        message=render_to_string('auth/activate.html',{
           'user':user,
           'domain':'127.0.0.1:8000',
           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
           'token':generate_token.make_token(user)
        }) 
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request, "For activation click link in your email")
        return redirect('/auth/login')

    return render(request, 'auth/signup.html')

 
class ActivateAccountView(View):
 def get(self, request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Activation completed")
        return redirect('/auth/login')
    return render(request, 'auth/activatefail.html')
       



# to change password

class RequestRestEmailView(View):
   def get(self,request):
      return render(request, 'auth/request-reset-email.html')
   
   def post(self, request):
      email= request.POST['email']
      user = User.objects.filter(email=email)

      if user.exists():
         current_site = get_current_site(request)
         email_subject='Rest our Password'
         message=render_to_string('auth/reset-user-password.html',{
           'domain':'127.0.0.1:8000',
           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
           'token':PasswordResetTokenGenerator().make_token(user[0])
         })

         email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
         EmailThread(email_message).start()
         messages.info(request,"Please check your mail")
         return render(request,'auth/request-reset-email.html')
      
class SetNewPasswordView(View):
   def get(self,request,uidb64,token):
      context={
         'uidb64':uidb64,
         'token':token
      }
      try:
         user_id= force_str(urlsafe_base64_decode(uidb64))
         user=User.objects.get(pk=user_id)

         if not PasswordResetTokenGenerator().check_token(user,token):
            messages.warning(request,"Invalid link, Please try again after sometime ")
            return render(request,'auth/request-reset-email.html')
      except DjangoUnicodeDecodeError as identifier:
         pass
      return render(request,'auth/set-new-password.html',context)
   
   
   def post(self,request,uidb64,token):
      context={
         'uidb64':uidb64,
         'token':token,
        }
      password         = request.POST.get('pass1')
      confirm_password = request.POST.get('pass2')

        # Ensure passwords match
      if password!= confirm_password:
            messages.warning(request, "Passwords do not match.")
            return render(request, 'auth/set-new-password.html')
      try:
         user_id = force_str(urlsafe_base64_decode(uidb64))
         user=User.objects.get(pk=user_id)
         user.set_password(password)
         user.save()
         messages.success(request, "password successfull changed")
         return redirect('/auth/login')
      
      except DjangoUnicodeDecodeError as idenifier:
         messages.warning(request,"somtimg went wrong")
         return render(request, 'auth/set-new-password.html',context)
      
def OtpVerification(request):
   return render(request,'auth/otpverification.html')



def loogin(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=uname, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log in success")
            request.session['is_authenticated'] = True

            # Redirect to the product details page or a default URL if 'next' not present
            next_param = request.GET.get('next')

            if next_param:
             return redirect(next_param)
            else:
               return redirect('/mainapp/index')

        else:
            messages.warning(request, "Incorrect User Information")
            return redirect('/auth/login')

    return render(request, 'auth/login.html')


def loogout(request):
   vkart_loogout(request)
   messages.success(request,"Log in to enjoy more")
   return redirect('/auth/login')