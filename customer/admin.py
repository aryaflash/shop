from django.contrib import admin
from .models import Customer, Cart
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Customer)
admin.site.register(Cart)
TokenAdmin.raw_id_fields = ['user']