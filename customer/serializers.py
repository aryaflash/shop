from rest_framework import serializers
from .models import Customer, Cart

class CustomerRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type' : 'password'}, write_only = True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phoneNumber', 'address', 'town', 'state', 'zipcode', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }


    def save(self):
        password =self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'passwords donot match'})
        customer = Customer(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            phoneNumber = self.validated_data['phoneNumber'],
            address = self.validated_data['address'],
            town = self.validated_data['town'],
            state = self.validated_data['state'],
            zipcode = self.validated_data['zipcode'],
        )
        customer.set_password(self.validated_data['password'])
        customer.save()

        return customer


class CartSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source = 'customer.phoneNumber')
    class Meta:
        model = Cart
        fields = ['customer', 'item_id', 'quantity', 'purchased']
