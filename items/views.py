from rest_framework import generics
from .serializers import ItemSerializer
from rest_framework import permissions
from .models import Item
from .permissions import IsOwnerOrReadOnly

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
