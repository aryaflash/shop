from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('shop/customer/register/', views.CustomerRegister.as_view(), name = "Customer_Register"),
    path('shop/customer/<int:pk>/', views.CustomerDetail.as_view(), name = "Customer_Detail"),
    path('shop/customer/login/', obtain_auth_token, name = "Customer_login"),
]