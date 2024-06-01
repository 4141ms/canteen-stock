from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 菜单
class Menu(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField()

# 角色
class Role(models.Model):
    name = models.CharField(max_length=128)
    flag = models.CharField(max_length=128)
    sys_menus = models.ManyToManyField("SysMenu")


# 系统菜单
class SysMenu(models.Model):
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)

# 用户信息
class UserInfo(models.Model):
    # 定义一个一对一的外键
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # 对应角色表里的flag
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=128)