from django.urls import path
from .views import supplierList
from property import views

urlpatterns = [
    # 显示供货商列表
    path('suppliers/', supplierList, name='supplier_list'),
    # 创建新订单
    path('newOrder/', views.createOrderSet, name='createOrderSet'),
    # 返回库存列表
    path('showStock/', views.stockOptionSet, name='createOrderSet'),
    # 修改库存
    path('editStock/', views.editStock, name='editStock'),
    # 删除库存
    path('delStock/', views.delStock, name='delStock'),
    
    # 返回订单列表
    path('showOrder/', views.showOrder, name='showOrder'),
    # 删除订单
    path('delOrder/', views.delOrder, name='showOrder'),
    
    
    
    
]
