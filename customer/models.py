from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class CustomerManager(BaseUserManager):
    def create_user(self, username, email, phoneNumber, address, town, state, zipcode, password = None ):
        if not username:
            raise ValueError("USers must have username")
        if not email:
            raise ValueError("USers must have email")
        if not phoneNumber:
            raise ValueError("USers must have phoneNumber")
        if not address:
            raise ValueError("USers must have address")
        if not town:
            raise ValueError("USers must have town")
        if not state:
            raise ValueError("USers must have state")
        if not zipcode:
            raise ValueError("USers must have zipcode")
        if not password:
            raise ValueError("USers must have password")
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            phoneNumber = phoneNumber,
            address = address,
            town = town,
            state = state,
            zipcode = zipcode,
            )

        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, email, phoneNumber, address, town, state, zipcode, password):
        if not username:
            raise ValueError("USers must have username")
        if not email:
            raise ValueError("USers must have email")
        if not phoneNumber:
            raise ValueError("USers must have phoneNumber")
        if not address:
            raise ValueError("USers must have address")
        if not town:
            raise ValueError("USers must have town")
        if not state:
            raise ValueError("USers must have state")
        if not zipcode:
            raise ValueError("USers must have zipcode")
        if not password:
            raise ValueError("USers must have password")

        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            phoneNumber = phoneNumber,
            address = address,
            town = town,
            state = state,
            zipcode = zipcode,
            password = password
            )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user





class Customer(AbstractBaseUser):
    username = models.CharField(max_length = 50, blank = False)
    email = models.EmailField(unique = True, validators = ([EmailValidator]), blank = False)
    phoneNumber = models.BigIntegerField(unique = True, primary_key = True, blank = False)
    address = models.CharField(max_length = 50, blank = False)
    town = models.CharField(max_length = 50, blank = False)
    state = models.CharField(max_length = 50, blank = False)
    zipcode = models.IntegerField(blank = False)
    password_reset_code = models.CharField(max_length = 6, blank = True)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)


    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = ['username', 'email', 'address', 'town', 'state', 'zipcode']

    objects = CustomerManager()


    def __str__(self):
        return self.username + " " + self.email + " " + str(self.phoneNumber) + " " + self.address + " " + self.town + " " + self.state + " " + str(self.zipcode) + " " + self.password


    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = "cart")
    item_id = models.IntegerField()
    quantity = models.IntegerField(default = 0)
    purchased = models.BooleanField(default = False)