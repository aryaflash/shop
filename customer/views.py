from rest_framework.response import Response
from rest_framework.views import  APIView
from .serializers import CustomerRegisterSerializer
from .models import Customer
from rest_framework import generics
from rest_framework.authtoken.models import Token
# Create your views here.

class CustomerRegister(APIView):
    def post(self, request, format = None):
        serializer = CustomerRegisterSerializer(data = request.data)
        rdata = {}
        if serializer.is_valid():
            customer = serializer.save()
            rdata['response'] = "successfully registered user"
            rdata['name'] = customer.username
            rdata['phoneNumber'] = customer.phoneNumber
            token = Token.objects.get(user = customer).key
            rdata['token'] = token
        else:
            rdata = serializer.errors
        return Response(rdata)
    
    def get(self, request, format = None):
        customer = Customer.objects.all()
        serializer = CustomerRegisterSerializer(customer, many = True)
        return Response(serializer.data)

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer
