from django.shortcuts import render
from django.views import View
from backend.models import Menu, UserInfo, User, Role, SysMenu
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json

# Create your views here.

#展示菜单
def showMenu(request):
    response = {}

    menus = Menu.objects.all()
    response['menus'] = json.loads(serializers.serialize("json", menus))
    
    return JsonResponse(response)

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
                    "username": user.username,
                    "email": user.email,
                    "avatar_url": userInfo.avatar_url
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
                return JsonResponse(response)
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

# @csrf_exempt
def test1(request):
    response = {}
    # user=User.objects.get(id=3)
    # role = Role.objects.filter(flag="CUSTOMER").first()
    # userInfo = UserInfo(user=user, role=role)
    # userInfo.save()
    # print(UserInfo.objects.get(id=4).user.username)
    return JsonResponse({
                'code': 403,
                "msg": '测试接口'
            })