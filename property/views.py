from django.shortcuts import render
from property.models import Supplier

from django.http import JsonResponse
from django.core import serializers
from backend.models import Order2Menu, Order, UserInfo, Menu, Stock, Menu2Stock2Number
import json
import datetime

# 展示供货商列表
def supplierList(request):
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
            time = datetime.datetime.now()
            order = Order.objects.create(user=UserInfo.objects.get(id=id), time=time.strftime("%Y-%m-%d %H:%M:%S"))
            sum = 0
            for dish in set:
                menu = Menu.objects.get(id=dish["id"])
                Order2Menu.objects.create(number=dish["num"], order=order, menu=menu)
                # 订单生成后，对库存原料做相应的更改！！！！
                raws = Menu2Stock2Number.objects.filter(menu=menu)
                try:
                    for raw in raws:
                        sim_num = raw.number
                        stock = raw.stock
                        stock.number = stock.number - sim_num * dish["num"]
                        stock.save()
                except:
                    return JsonResponse({
                        "code": 403,
                        "msg": "库存减少失败"
                    })
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
    
    
# 传递库存列表
def stockOptionSet(request):
    response = {}
    orders = []
    index = 0
    for raw in Stock.objects.all():
        index = index + 1
        tmp = {
            "id": raw.id,
            "index": index,
            "name": raw.name,
            "number": raw.number,
            "price": raw.price,
        }
        orders.append(tmp)
    response['stocks']=orders
    return JsonResponse(response)




# 修改库存
def editStock(request):
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
            if "id" in json_data.keys():
                stock_id =  json_data.get("id")
                stock = Stock.objects.get(id=stock_id)
                stock.name = json_data.get("name")
                stock.price = json_data.get("price")
                stock.number = json_data.get("number")
                stock.save()
            else:
                stock = Stock(name=json_data.get("name"), price=json_data.get("price"), number=json_data.get("number"))
                stock.save()
                
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                    'code': 403,
                    "msg": '库存修改失败'
                })
    return JsonResponse({
                    'code': 200,
                    "msg": '库存修改成功'
                })

# 删除库存
def delStock(request):
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
            
        except:
            return JsonResponse({
                'code': 403,
                "msg": '删除失败'
            })
        stock = Stock.objects.get(id=json_data)
        stock.delete()
        return JsonResponse({
            'code': 200,
            "msg": '删除成功'
        })

# 展示订单
def showOrder(request):
    response = {}
    orders = []
    index = 0
    sum = 0
    for order in Order.objects.all():
        index = index + 1
        tmp = {
            "id": order.id,
            "index": index,
            "username": order.user.user.username,
            "time": order.time,
            "total": order.total,
        }
        sum = sum + order.total
        orders.append(tmp)
    response['orders']=orders
    response['total']=sum
    return JsonResponse(response)


# 删除订单
def delOrder(request):
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
            
        except:
            return JsonResponse({
                'code': 403,
                "msg": '删除失败'
            })
        order = Order.objects.get(id=json_data)
        order.delete()
        return JsonResponse({
            'code': 200,
            "msg": '删除成功'
        })