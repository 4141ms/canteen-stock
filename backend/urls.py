from django.urls import path
from backend import views

urlpatterns = [#匹配url时，从上往下查找，找到第一个后停止
    # 登录界面
    path("login/", views.login, name="login"),
    # 注册界面
    path("register/", views.register, name="register"),
    # 更新用户信息
    path("updateUserInfo/", views.updateUserInfo, name="updateUserInfo"),
    # 根据用户id获取用户信息
    path("getUserById/", views.getUserById, name="getUserById"),


    # 上传菜品图像
    path("load_dish/", views.loadDishImage, name="loadDishImage"),
    # 获取菜品图片
    path("download_dish/<str:path>/", views.downloadDish, name="downloadDish"),
    
    # 图表：返回库存数据
    path("stock_map_data/", views.stockMapData, name="stockMapData"),
    # 图表：返回季度营业额数据
    path("turnover_map_data/", views.turnoverMapData, name="turnoverMapData"),
   
    # 图表：返回菜品数据
    path("dish_map_data/", views.dishMapData, name="dishMapData"),
   
    
    
    
    # 测试接口
    path("test/", views.test1, name="test"),

]