from django.urls import path
from feedback import views

urlpatterns = [#匹配url时，从上往下查找，找到第一个后停止
    #展示所有反馈信息
    path("feedback_list/", views.feedback_list, name="feedback_list"),
    #创建反馈信息
    path("create_feedback/", views.create_feedback, name="create_feedback"),
    #删除反馈信息
    path("delete_feedback/", views.delete_feedback, name="delete_feedback"),
    #修改反馈信息
    path("update_feedback/", views.update_feedback, name="update_feedback"),
]