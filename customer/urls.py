from django.urls import path
from . import views



urlpatterns = [
    #customer registration
    path('shop/customer/register/', views.CustomerRegister.as_view(), name = "Customer_Register"),
    #only superusers can access
    #users list
    path('shop/customer/', views.CustomerList.as_view(), name = 'Customer_List'),
    #superusers along with respective customer can access
    path('shop/customer/<int:pk>/', views.CustomerDetail.as_view(), name = "Customer_Detail"),
    path('shop/customer/login/', views.CustomAuthToken.as_view(), name = "Customer_login"),
    #only superusers can access
    #superusers list
    path('shop/superuser/', views.SuperUserList.as_view(), name = 'SuperUser_List'),
    #only respective customers can access
    #users can add items to their cart
    path('shop/customer/cartadd/', views.CartCreate.as_view(), name = 'Cart_Create'),
    #superusers along with respective customer can access
    path('shop/customer/cart/<int:pk>/', views.CartDetail.as_view(), name = 'Cart_Detail'),
    #only superusers can access
    #complete list of all items in all carts
    path('shop/cart/', views.CartList.as_view(), name = 'Cart_List'),
    #only respected users can access
    #list of items in respective carts
    path('shop/customer/cart/', views.CustomerCartList.as_view(), name = 'CustomerCart_List'),
    path('shop/customer/reset/', views.CustomerPasswordReset.as_view(), name = "Customer_Password_Reset"),
    path('shop/customer/code/', views.CustomerCodeCheck.as_view(), name = 'Customer_Code_Check'),
    path('shop/customer/rpass/', views.CustomerNewPassword.as_view(), name = 'Customer_New_Password'),

    
]