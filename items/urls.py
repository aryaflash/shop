from django.urls import path, include
from . import views

urlpatterns = [
    path('shop/items/', views.ItemList.as_view(), name = 'Item_List'),
    path('shop/items/<int:pk>/', views.ItemDetail.as_view(), name = 'Item_Detail'),
    
]