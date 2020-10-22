from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'Large', 'Medium', 'Small', 'Ldimension', 'Mdimension', 'Sdimension', 'colour', 'painted', 'Lprice', 'Mprice', 'Sprice', 'Lstock', 'Mstock', 'Sstock', 'lid', 'material', 'description']
