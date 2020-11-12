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
from rest_framework import status
load_dotenv()
import os
import random


# Create your views here.

class CustomerRegister(APIView):
    permission_classes = []
    def post(self, request, format = None):
        serializer = CustomerRegisterSerializer(data = request.data)
        values = {}
        if serializer.is_valid():
            customer = serializer.save()
            values['response'] = "successfully registered user"
            values['name'] = customer.username
            values['email'] = customer.email
            token = Token.objects.get(user = customer).key
            values['token'] = token
            data = [{'status' : status.HTTP_200_OK, 'values' : values, 'message' : 'OK'}]
            return Response(data)
        else:
            values = serializer.errors
            data = [{'status' : status.HTTP_400_BAD_REQUEST, 'values' : values, 'message' : 'DATA NOT VALID'}]
        return Response()
    
class CustomerList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        if request.user.is_superuser == False:
            data = [{'status' : status.HTTP_401_UNAUTHORIZED, 'values' : [], 'message' : 'UNAUTHORIZED'}]
            return Response(data)
        customer = Customer.objects.filter(is_superuser = False)
        serializer = CustomerRegisterSerializer(customer, many = True)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
        return Response(data)

class SuperUserList(APIView):
    def get(self, request, format = None):
        if request.user.is_superuser == False:
            data = [{'status' : status.HTTP_401_UNAUTHORIZED, 'values' : [], 'message' : 'UNAUTHORIZED'}]
            return Response(data)
        customer = Customer.objects.filter(is_superuser = True)
        serializer = CustomerRegisterSerializer(customer, many = True)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
        return Response(data)
    

class CustomerDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk = pk)
        except Customer.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
        return Response(data)

    def put(self, request, pk, format = None):
        customer =  self.get_object(pk)
        serializer = CustomerSerializer(instance = customer, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
            return Response(data)
        data = [{'status' : status.HTTP_400_BAD_REQUEST, 'values' : [], 'message' : 'DATA NOT VALID'}]
        return Response(data = data)

    def delete(self, request, pk, format = None):
        customer = self.get_object(pk = pk)
        customer.delete()
        data = [{'status' : status.HTTP_204_NO_CONTENT, 'values' : [], 'message' : 'DELETED'}]
        return Response(data)
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data, context = {'request' : request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)
        values = [{
            'email'  : user.pk,
            'username' : user.username,
            'token'    : token.key,
            }]
        data = [{'status' : status.HTTP_200_OK, 'values' : values, 'message' : 'OK'}]
        return Response(data = data)


class CartCreate(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, format = None):
        serializer = CartSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
            return Response(data)
        data = [{'status' : status.HTTP_400_BAD_REQUEST, 'values' : [], 'message' : 'DATA NOT VALID'}]
        return Response(data = data)

    def perform_create(self, serializer):
        serializer.save(customer = self.request.user)

class CartList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        if request.user.is_superuser == False:
            data = [{'status' : status.HTTP_401_UNAUTHORIZED, 'values' : [], 'message' : 'UNAUTHORIZED'}]
            return Response(data)
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many = True)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
        return Response(data)


class CartDetail(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def get_object(self, pk):
        try:
            return Cart.objects.get(customer = pk)
        except Cart.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
        return Response(data)

    def put(self, request, pk, format = None):
        cart =  self.get_object(pk)
        serializer = CartSerializer(instance = cart, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
            return Response(data)
        data = [{'status' : status.HTTP_400_BAD_REQUEST, 'values' : [], 'message' : 'DATA NOT VALID'}]
        return Response(data = data)

    def delete(self, request, pk, format = None):
        cart = self.get_object(pk = pk)
        cart.delete()
        data = [{'status' : status.HTTP_204_NO_CONTENT, 'values' : [], 'message' : 'DELETED'}]
        return Response(data)
    

class CustomerCartList(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def get(self, request, format = None):
        cart = Cart.objects.filter(customer = request.user)
        print(request.user)
        serializer = CartSerializer(cart, many = True)
        data = [{'status' : status.HTTP_200_OK, 'values' : serializer.data, 'message' : 'OK'}]
        return Response(data)
        

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
        data = [{'status' : status.HTTP_200_OK, 'values' : [{'email' : email}], 'message' : 'code has been sent to gmail to reset password'}]
        return Response(data = data)

class CustomerCodeCheck(APIView):
    permission_classes = []
    def post(self, request, format = None):
        email = request.data['email']
        try:
            customer = Customer.objects.get(email = email)
        except Customer.DoesNotExist:
            raise Http404
        if customer.password_reset_code != request.data['code']:
            data = [{'status' : status.HTTP_400_BAD_REQUEST, 'values' : [], 'message' : 'WRONG CODE'}]
            return Response(data)
        values = {'email' : email, 'code' : request.data['code']}
        data = [{'status' : status.HTTP_200_OK, 'values' : values, 'message' : 'OK'}]
        return Response(data = data)


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
            data = [{'status' : status.HTTP_400_BAD_REQUEST, 'values' : [], 'message' : 'WRONG CODE'}]
            return Response(data)
        password = request.data['password']
        password2 = request.data['password2']
        if password != password2:
            raise ValidationError({'password' : 'passwords do not match'})
        customer.password_reset_code = ""
        customer.set_password(password)
        customer.save()
        data = [{'status' : status.HTTP_201_CREATED, 'values' : [], 'message' : 'OK'}]
        return Response(data = data)
        