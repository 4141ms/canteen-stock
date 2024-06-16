from django.urls import path
from .views import supplier_list
from property import views

urlpatterns = [
    # 显示供货商列表
    path('suppliers/', supplier_list, name='supplier_list'),
    # 创建新订单
    path('newOrder/', views.createOrderSet, name='createOrderSet'),
    
]
