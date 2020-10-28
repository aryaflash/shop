from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class IsCustomer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.phoneNumber == request.user.phoneNumber

# class IsSuperUser(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         print("hi")
#         print(request.user.is_superuser)
#         if request.user.is_superuser == True:
#             return True
#         return False