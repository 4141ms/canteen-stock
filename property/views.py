from django.shortcuts import render
from property.models import Supplier

from django.http import JsonResponse
from django.core import serializers
from backend.models import Order2Menu, Order, UserInfo, Menu
import json
import datetime

# 展示供货商列表
def supplier_list(request):
    response = {}

    suppliers = Supplier.objects.all()
    response['suppliers'] = json.loads(serializers.serialize("json", suppliers))
    
    return JsonResponse(response)

# 生成新订单
def createOrderSet(request):
    response = {}
    if request.method == "POST":
        # 数据在request.body里
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                    'code': 403,
                    "msg": '用户认证失败'
                })
        data = json_data.get("params")
        id = data.get("id")
        set = data.get("data")
        try: 
           # 创建新订单
            order = Order.objects.create(user=UserInfo.objects.get(id=id), time=datetime.datetime.now())
            sum = 0
            for dish in set:
                menu = Menu.objects.get(id=dish["id"])
                Order2Menu.objects.create(number=dish["num"], order=order, menu=menu)
                sum = sum + dish["price"] * dish["num"]
            order.total = sum
            order.save()
        except:
            return JsonResponse({
                "code": 403,
                "msg": "订单创建失败"
            })
    return JsonResponse({
        "code": 200,
        "msg": "订单创建成功"
    })