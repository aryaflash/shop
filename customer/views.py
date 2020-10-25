from rest_framework.response import Response
from rest_framework.views import  APIView
from .serializers import CustomerRegisterSerializer, CartSerializer
from .models import Customer, Cart
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsCustomer
from rest_framework.decorators import permission_classes
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
    
class CustomerList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        if request.user.is_superuser == False:
            return Response({'error' : 'you dont have permission'})
        customer = Customer.objects.filter(is_superuser = False)
        serializer = CustomerRegisterSerializer(customer, many = True)
        return Response(serializer.data)

class SuperUserList(APIView):
    def get(self, request, format = None):
        if request.user.is_superuser == False:
            return Response({'error' : 'you dont have permission'})
        customer = Customer.objects.filter(is_superuser = True)
        serializer = CustomerRegisterSerializer(customer, many = True)
        return Response(serializer.data)
    

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data, context = {'request' : request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)
        print(user)
        return Response({
            'token'    : token.key,
            'user_id'  : user.pk,
            'username' : user.username,
            'message'  : 'login successful'

        })


class CartCreate(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(customer = self.request.user)

class CartList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        if request.user.is_superuser == False:
            return Response({'error' : 'you dont have permission'})
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many = True)
        return Response(serializer.data)


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CustomerCartList(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def get(self, request, format = None):
        cart = Cart.objects.filter(customer = request.user)
        serializer = CartSerializer(cart, many = True)
        return Response(serializer.data)
        