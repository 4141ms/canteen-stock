from django.shortcuts import render
from django.views import View
from backend.models import Menu
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.

#展示菜单
def showMenu(request):
    response = {}

    menus = Menu.objects.all()
    response['menus'] = json.loads(serializers.serialize("json", menus))
    
    return JsonResponse(response)