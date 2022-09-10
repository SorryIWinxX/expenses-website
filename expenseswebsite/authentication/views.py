from ast import Expression
from curses.ascii import isalnum
import email
from importlib.resources import path
from lib2to3.pgen2 import token
from multiprocessing import context
from operator import truediv
from os import link
from urllib import request
from django.shortcuts import render, redirect
from django.views import View
import json
import django.http 
from json_response import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from .utils import account_activation_token
from django.contrib import auth



# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error':'Sorry your email in use, please choose another email'},status=409)   
        return JsonResponse({'email_valid':True})

class VerificationView(View):
        def get(self, request, uidb64, token):

            try:
                id=force_str(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=id)

                if not account_activation_token.check_token(user, token):
                    return redirect('login'+'?message='+'User already activated')

                if user.is_active:
                    return redirect('login')
                user.is_active = True
                user.save()

                messages.success(request, 'Account Activated succesfully')
                return redirect('login')

            except Exception as ex:
                pass

            

            return redirect('login')

class LoginView(View):
        def get(self, request):
            return render(request, 'authentication/login.html')
        
        def post(self,request):
            username=request.POST['username']
            password= request.POST['password']

            if username and password:
                user=auth.authenticate(username=username, password=password)

                if user:
                    if user.is_active:
                        auth.login(request, user)
                        messages.success(request, 'Welcolme, '+
                                user.username + ' you are now logged in')

                        return redirect('expenses')

                    messages.error(request,'Account is no activate, please check your email')
                    return render(request, 'authentication/login.html')
                messages.error(request,'Invalid credentials, try again')
                return render(request, 'authentication/login.html')

            messages.error(request,'Please fill all fields')
            return render(request, 'authentication/login.html')

class UserNameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contains alphanumeric characters'},status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'Sorry your username in use, please choose another username'},status=409)   
        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')


    def post(self, request):
        #GET USER DATA
        #VALIDATE
        #Create a user account

        username= request.POST['username']
        email = request.POST['email']
        password = request.POST['password']


        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password)<6:
                    messages.error(request, 'Password to short')
                    return render(request, 'authentication/register.html',context)
                    

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()



                #path_to View
                #- getting domain we are on
                #- relative url to verification
                #- encode uid
                #- token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link= reverse('activate', kwargs={'uidb64':uidb64, 
                'token':account_activation_token.make_token(user)})


                email_subject ='Activate your account'

                activate_url= 'http://'+domain+link

                email_body='Hi'+user.username + 'Please use this link to verify your account \n' + activate_url



                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )

                email.send(fail_silently=False)

                messages.success(request, 'Account succesfully created')
                return render(request, 'authentication/register.html')
                    

        return render(request, 'authentication/register.html')
        

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')