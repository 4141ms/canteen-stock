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

# 登录界面(已改phone)
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
                    "phone":userInfo.phone,
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
    
# 注册界面(已改phone)
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
        phone = json_data.get("phone")
        try:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            t_role = json_data.get("role")
            role = Role.objects.filter(flag=t_role).first()
            userInfo = UserInfo(user=user, role=role,phone=phone)
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

# 更新用户信息(已加phone) fyt
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
        phone = json_data.get("phone")
        #头像
        #avatar_url = json_data.get("avatar_url")

        if username:
            userInfo.user.username = username
        if email:
            userInfo.user.email = email
        if password:
            userInfo.user.password = password
        if phone:
            userInfo.phone = phone
        
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
                "phone":userInfo.phone,
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

# 根据用户id获取用户信息(已改phone) fyt
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
                "phone":userInfo.phone,
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
 
# 显示角色列表 fyt
# def showRole(request):
#     response = {}
    
#     return JsonResponse(response)

# 反馈信息



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


