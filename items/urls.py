from django.urls import path, include
from . import views

urlpatterns = [
    path('shop/items/', views.ItemList.as_view(), name = 'Item_List'),
    path('shop/items/<int:pk>/', views.ItemDetail.as_view(), name = 'Item_Detail'),
    #only superusers can access
    path('shop/items/edit/<int:pk>/', views.ItemUpdateDelete.as_view(), name = 'Item_Update_Delete')
]