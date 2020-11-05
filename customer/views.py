from rest_framework.response import Response
from rest_framework.views import  APIView
from .serializers import CustomerRegisterSerializer, CartSerializer, CustomerSerializer
from .models import Customer, Cart
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwner, IsCustomer
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from dotenv import load_dotenv
from django.http import Http404
from django.core.exceptions import ValidationError
load_dotenv()
import os
import random


# Create your views here.

class CustomerRegister(APIView):
    permission_classes = []
    def post(self, request, format = None):
        serializer = CustomerRegisterSerializer(data = request.data)
        rdata = {}
        if serializer.is_valid():
            customer = serializer.save()
            rdata['response'] = "successfully registered user"
            rdata['name'] = customer.username
            rdata['email'] = customer.email
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
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data, context = {'request' : request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)
        return Response({
            'email'  : user.pk,
            'username' : user.username,
            'token'    : token.key,
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
        

class CustomerPasswordReset(APIView):
    permission_classes = []
    def random_num_gen(self):
        x = ""
        for i in range(0,6):
            x += str(random.randint(0, 9))
        return x

    def post(self, request, format = None):
        email = request.data['email']
        try:
            customer =  Customer.objects.get(email = email)
        except Customer.DoesNotExist:
            raise Http404
        code = self.random_num_gen()
        send_mail('Password Reset', code, os.environ.get('EMAIL_HOST_USER'), [email], fail_silently = False)
        customer.password_reset_code = code
        customer.save()
        return Response({'data' : 'code has been sent to gmail to reset password',
                        'email' : email})

class CustomerCodeCheck(APIView):
    permission_classes = []
    def post(self, request, format = None):
        email = request.data['email']
        try:
            customer = Customer.objects.get(email = email)
        except Customer.DoesNotExist:
            raise Http404
        if customer.password_reset_code != request.data['code']:
            return Response({'error':'please enter correct code'})
        return Response({'data' : 'code verified','email' : email, 'code' : request.data['code']})


class CustomerNewPassword(APIView):
    permission_classes = []
    def post(self, request, format = None):
        email = request.data['email']
        code = request.data['code']
        try:
            customer = Customer.objects.get(email = email)
        except Customer.DoesNotExist:
            raise Http404
        if customer.password_reset_code != code:
            return Response({'data' : 'code authentication error'})
        password = request.data['password']
        password2 = request.data['password2']
        if password != password2:
            raise ValidationError({'password' : 'passwords do not match'})
        customer.password_reset_code = ""
        customer.set_password(password)
        customer.save()
        return Response({'data' : 'password successfully changed'})

    
