from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'colour', 'painted', 'material', 'lid', 'description', 'updated', 'Large', 'Medium', 'Small', 'Lprice', 'Mprice', 'Sprice', 'Ldimension', 'Mdimension', 'Sdimension', 'Lstock', 'Mstock', 'Sstock']
