from django.urls import path
from backend import views

urlpatterns = [#匹配url时，从上往下查找，找到第一个后停止
    # 显示菜单视图
    path("show_menu/", views.showMenu, name="show_menu"),
    # 登录界面
    path("login/", views.login, name="login"),
    # 注册界面
    path("register/", views.register, name="register"),
    # 测试接口
    path("test/", views.test1, name="test"),
    # # 详情视图
    # path("<int:id>", views.student),
    # path("search/", views.StudentSearchView.as_view()),
    # # 表单搜索
    # path("t_search/", views.FormView.as_view()),
    # # 添加学生数据
    # path("add/", views.add_student, name="add_student"),
    # # 编辑学生数据
    # path("<int:id>-edit/", views.edit_student, name="edit_student"),
    # # 删除学生数据 
    # path("delete/", views.DeleteStudentView.as_view(), name="delete_student"),
    # # 注册添加用户
    # path("register/", views.RegisterView.as_view()),
    # path("userlist/", views.showUserInfo, name="user_list")
]