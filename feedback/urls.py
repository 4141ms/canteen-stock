from django.urls import path
from feedback import views

urlpatterns = [#匹配url时，从上往下查找，找到第一个后停止
    #提交反馈信息
     path("create_feedback/", views.create_feedback, name="create_feedback"),

    # 显示菜单视图
    # path("show_menu/", views.showMenu, name="show_menu"),
    # 登录界面
    # path("login/", views.login, name="login"),
    
]