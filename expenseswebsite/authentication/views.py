from curses.ascii import isalnum
from django.shortcuts import render
from django.views import View
import json
import django.http 
from json_response import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
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