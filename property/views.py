from django.shortcuts import render
from property.models import Supplier

from django.http import JsonResponse
from django.core import serializers
import json

# 展示供货商列表
def supplier_list(request):
    response = {}

    suppliers = Supplier.objects.all()
    response['suppliers'] = json.loads(serializers.serialize("json", suppliers))
    
    return JsonResponse(response)