from locale import currency
from pathlib import Path
from django.contrib import messages
from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference

# Create your views here.


def index(request):



    if request.method=='GET':
        currency_data=[]
        file_path=Path(settings.BASE_DIR, 'currencies.json')

        with open(file_path,'r') as json_file:

           data = json.load(json_file)

           for k,v in data.items():
                currency_data.append({'name':k, 'value':v})
        return render(request,'preferences/index.html',{'currencies':currency_data})
    else:
        currency=request.POST['currency']
        messages.success(request,'Changes saved')