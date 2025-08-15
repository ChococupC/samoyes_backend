from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        user_obj = request.user
        print(request.auth)
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        print(self, "has_object_permission")
        print(request, "has_object_permission")
        print(view, "has_object_permission")
        print(obj, "has_object_permission")

        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
