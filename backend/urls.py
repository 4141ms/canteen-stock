from django.urls import path
from backend import views

urlpatterns = [#匹配url时，从上往下查找，找到第一个后停止
    # 登录界面
    path("login/", views.login, name="login"),
    # 注册界面
    path("register/", views.register, name="register"),
    # 根据id返回用户信息
    path("<int:id>-userInfo/", views.getUserById, name="userInfo"),

    # 显示菜单视图
    path("show_menu/", views.showMenu, name="show_menu"),
    # 传递原料选项
    path("raw_set/", views.rawOptionSet, name="rawOptionSet"),
    # 修改菜品对应的原材料
    path("edit_menu_raw/", views.editMenuToRaw, name="editMenuToRaw"),
    # 删除菜品对应的原材料
    path("del_menu_raw/", views.delMenuToRaw, name="delMenuToRaw"),

    # 修改菜单
    path("edit_menu/", views.editMenu, name="editMenu"),
    # 删除菜品
    path("del_menu/", views.delMenu, name="delMenu"),
    
    # 上传用户头像
    path("load_ava/", views.getUserProfiles, name="getUserProfiles"),
    # 获取用户头像
    path("download_ava/<str:path>/", views.downloadAva, name="downloadAva"),
    

    # 更新用户信息
    path("updateUserInfo/", views.updateUserInfo, name="updateUserInfo"),
    # 根据用户id获取用户信息
    path("getUserById/", views.getUserById, name="getUserById"),


    # 上传菜品图像
    path("load_dish/", views.loadDishImage, name="loadDishImage"),
    # 获取菜品图片
    path("download_dish/<str:path>/", views.downloadDish, name="downloadDish"),
    
    
    
    # 测试接口
    path("test/", views.test1, name="test"),

]