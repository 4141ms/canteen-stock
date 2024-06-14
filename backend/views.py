from django.shortcuts import render
from django.views import View
from backend.models import Menu, UserInfo, User, Role, SysMenu, Menu2Stock2Number, Stock
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
import os
import uuid
from urllib.parse import unquote

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 生成8位uuid
def generate_unique_id():
    unique_id = uuid.uuid4().hex[:8]
    return unique_id
# Create your views here.

# 登录界面
@csrf_exempt
def login(request):
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
        
        username = json_data.get("username")
        password = json_data.get("password")
        # 用户已存在
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                userInfo = UserInfo.objects.filter(user=user).first()
                reUser = {
                    "id": userInfo.id,
                    "username": user.username,
                    "email": user.email,
                    "avatar_url": userInfo.avatar_url,
                    'phone': userInfo.phone
                }
                menus = []
                role = userInfo.role
                for menu in role.sys_menus.all():
                    tmp = {
                        "id": menu.pk,
                        "name": menu.name,
                        "path": menu.path
                    }
                    menus.append(tmp)
                
                response["code"] = 200
                response["user"] = reUser
                response["role"] = role.flag
                response["menus"] = menus
                return JsonResponse(response, json_dumps_params={'ensure_ascii':False})
            else:
                return JsonResponse({
                    'code': 403,
                    "msg": '用户认证失败'
                })
        # 用户不存在
        else:
            response["user"] = "fail"
            return JsonResponse(response)
    
# 注册界面
@csrf_exempt
def register(request):
    response = {}
    if request.method == "POST":
        # 数据在request.body里
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                    'code': 403,
                    "msg": '注册失败'
                })
        
        username = json_data.get("username")
        email = json_data.get("email")
        password = json_data.get("password")
        try:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            t_role = json_data.get("role")
            role = Role.objects.filter(flag=t_role).first()
            userInfo = UserInfo(user=user, role=role)
            userInfo.save()
            return JsonResponse({
                'code': 200,
                "msg": '用户创建成功'
            })
        except Exception:
            return JsonResponse({
                'code': 403,
                "msg": '用户创建失败'
            })

# 更新用户信息 fyt
def updateUserInfo(request):
    response = {}
    # 除了基本信息还有头像（可以先不考虑）
    if request.method == "POST":
        # 数据在request.body里
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                'code': 403,
                "msg": '请求数据格式错误'
            })
        
        user_id = json_data.get("id")

        userInfo = UserInfo.objects.get(id=user_id)

        try:
            userInfo = UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'code': 404,
                "msg": '用户不存在'
            })

        # user = request.user
        username = json_data.get("username")
        email = json_data.get("email")
        password = json_data.get("password")
        #头像
        #avatar_url = json_data.get("avatar_url")

        if username:
            userInfo.user.username = username
        if email:
            userInfo.user.email = email
        if password:
            userInfo.user.password = password
        
        userInfo.user.save()
        userInfo.save()
        
        userInfo = UserInfo.objects.filter(id=user_id).first()
        #头像
        # if avatar_url:
        #     user_info.avatar_url = avatar_url
        # user_info.save()

        return JsonResponse({
            'code': 200,
            "msg": '用户信息更新成功',
            "user": {
                "id": userInfo.id,
                "username": userInfo.user.username,
                "email": userInfo.user.email,
                "password":'******',#不返回密码
                #头像
                #"avatar_url": user_info.avatar_url
            }
        })
    else:
        return JsonResponse({
            'code': 405,
            "msg": '仅支持POST请求'
        })

# 根据用户id获取用户信息 fyt
def getUserById(request):
    response = {}
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                'code': 403,
                "msg": '请求数据格式错误'
            })

        user_id = json_data.get("id")

        if not user_id:
            return JsonResponse({
                'code': 400,
                "msg": '用户ID未提供'
            })

        try:
            userInfo = UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'code': 404,
                "msg": '用户不存在'
            })

        return JsonResponse({
            'code': 200,
            "msg": '用户信息获取成功',
            "user": {
                "id": userInfo.id,
                "username": userInfo.user.username,
                "email": userInfo.user.email,
                # 如果有其他需要返回的信息，可以在这里添加,例：头像
                # "avatar_url": userInfo.avatar_url,
            }
        })
    else:
        return JsonResponse({
            'code': 405,
            "msg": '仅支持POST请求'
        })
 
#展示菜单
def showMenu(request):
    response = {}

    # menus = Menu.objects.all()
    menus = []
    index = 0
    for menu in Menu.objects.all():
        index = index+1
        raws = []
        for raw in Menu2Stock2Number.objects.filter(menu=menu):
            t = {
                "raw_id": raw.id,
                "name": raw.stock.name,
                "number": raw.number
            }
            raws.append(t)
        tmp = {
                "id": menu.id,
                "index": index,
                "name": menu.name,
                "price": menu.price,
                "raw": raws
            }
        menus.append(tmp)
    response['menus'] = menus
    # response['menus'] = json.loads(serializers.serialize("json", menus))
    
    return JsonResponse(response)

# 传递库存列表
def rawOptionSet(request):
    response = {}
    options = []
    for raw in Stock.objects.all():
        tmp = {
            "id": raw.id,
            "name": raw.name
        }
        options.append(tmp)
    response['options']=options
    return JsonResponse(response)

# 修改菜品对应的原材料 
def editMenuToRaw(request):
    if request.method == "POST":
        # 数据在request.body里
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                    'code': 403,
                    "msg": '注册失败'
                })
        menu_id =  json_data.get("id")
        for raw in json_data.get("raws"):
            if 'raw_id' in raw.keys():
                raw_id = raw['raw_id']
                m2s = Menu2Stock2Number.objects.get(id=raw_id)
                stock = Stock.objects.get(name=raw['name'])
                m2s.number = raw['number']
                m2s.stock = stock
                m2s.save()
            else:
                menu = Menu.objects.get(id=menu_id)
                stock = Stock.objects.get(name=raw['name'])
                m2s = Menu2Stock2Number(menu=menu, stock=stock,number=raw['number'])
                m2s.save()
                raw['raw_id'] = m2s.id
        return JsonResponse({
                'code': 200,
                "msg": '修改成功',
                "data": json_data
        })
    
# 删除菜单对应的原材料
def delMenuToRaw(request):
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
            
        except:
            return JsonResponse({
                'code': 403,
                "msg": '删除失败'
            })
        m2s = Menu2Stock2Number.objects.get(id=json_data)
        m2s.delete()
        return JsonResponse({
            'code': 200,
            "msg": '删除成功'
        })
    
# 修改菜单
def editMenu(request):
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
            if "id" in json_data.keys():
                menu_id =  json_data.get("id")
                menu = Menu.objects.get(id=menu_id)
                menu.name = json_data.get("name")
                menu.price = json_data.get("price")
                menu.save()
            else:
                menu = Menu(name=json_data.get("name"), price=json_data.get("price"))
                menu.save()
                for raw in json_data.get("raw"):
                    stock = Stock.objects.get(name=raw['name'])
                    m2s = Menu2Stock2Number(menu=menu, stock=stock,number=raw['number'])
                    m2s.save()
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                    'code': 403,
                    "msg": '菜单修改失败'
                })
    return JsonResponse({
                    'code': 200,
                    "msg": '菜单修改成功'
                })

# 删除菜单
def delMenu(request):
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
            
        except:
            return JsonResponse({
                'code': 403,
                "msg": '删除失败'
            })
        menu = Menu.objects.get(id=json_data)
        menu.delete()
        return JsonResponse({
            'code': 200,
            "msg": '删除成功'
        })
    
# 上传图片
def getUserProfiles(request):
  
  if request.method == 'POST':
    if request.FILES:
      myFile =None
      for i in request.FILES:
        myFile = request.FILES[i]
      if myFile:
        dir = os.path.join(os.path.join(BASE_DIR, 'static'),'profiles')
        # print(myFile.type)
        destination = open(os.path.join(dir, generate_unique_id() + myFile.name),
                  'wb+')
        for chunk in myFile.chunks():
          destination.write(chunk)
        destination.close()
      return JsonResponse({
          'code': 200
      })
    
# 根据url返回头像文件
def downloadAva(request, path):
    import base64
    if request.method == 'GET':
        print(path)
        dir = os.path.join(os.path.join(BASE_DIR, 'static'),'profiles')
        file = open(os.path.join(dir, path), 'rb')
        print(file)
        result = file.read()
        return HttpResponse(result, content_type='image/jpeg')


# @csrf_exempt
def test1(request):
    response = {}
    m2s = Menu2Stock2Number.objects.get(id=1)
    print(m2s.stock.name, m2s.number)
    return JsonResponse({
                'code': 200,
                "msg": '测试接口'
            })


