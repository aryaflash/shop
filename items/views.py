from .serializers import ItemSerializer
from .models import Item
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter


class ItemList(APIView):
    permission_classes = []
    #search filter
    #override this
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name']

    def get(self, request, format = None):
        item = Item.objects.all()
        serializer = ItemSerializer(instance = item, many = True)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]

    def post(self, request, format = None):
        serializer = ItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
            return Response(data)


class ItemDetail(APIView):
    permission_classes = []
    def get_object(self, pk):
        try:
            return Item.objects.get(pk = pk)
        except Item.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
        return Response(data)

class ItemUpdateDelete(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk = pk)
        except Item.DoesNotExist:
            raise Http404

    def put(self, request, pk, format = None):
        if request.user.is_superuser == False:
            data = [{'status' : status.HTTP_401_UNAUTHORIZED, 'values' : [], 'message' : 'UNAUTHORIZED'}]
            return Response(data)
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
            return Response(data)
        data = [{'status' : status.HTTP_400_BAD_REQUEST, 'values' : [], 'message' : 'DATA NOT VALID'}]
        return Response(data = data)
    
    def delete(self, request, pk, format = None):
        if request.user.is_superuser == False:
            data = [{'status' : status.HTTP_401_UNAUTHORIZED, 'values' : [], 'message' : 'UNAUTHORIZED'}]
            return Response(data)
        item = self.get_object(pk = pk)
        item.delete()
        

    


