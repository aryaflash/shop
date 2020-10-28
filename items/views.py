from rest_framework import generics
from .serializers import ItemSerializer
from rest_framework import permissions
from .models import Item
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = []
    #search filter
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name']


class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = []

class ItemUpdateDelete(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk = pk)
        except Item.DoesNotExist:
            raise Http404

    def put(self, request, pk, format = None):
        if request.user.is_superuser == False:
            return Response({'error' : 'you dont have permission'})
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        if request.user.is_superuser == False:
            return Response({'error' : 'you dont have permission'})
        item = self.get_object(pk = pk)
        item.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    


