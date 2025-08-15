from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from datetime import timedelta

from my_app.user.models import User

class UsernameAuthentication(BaseAuthentication):

    def authenticate(self, request):
        username = request.query_params.get("username")
        user_obj = User.objects.filter(username=username).first()

        # Checking if user exist
        if not user_obj or user_obj.is_login == 0:
            raise AuthenticationFailed({"code": 400, "status": 200, "data": "", "message": "You have not login yet"})

        now = timezone.now()
        expire_time = user_obj.update_time + timedelta(minutes=30)

        # Checking if the expire_time falls within a range of 0 to 30 minutes
        if now >= expire_time:
            user_obj.is_login = 0
            user_obj.save()
            raise AuthenticationFailed({"code": 400, "status": 200, "data": "", "message": "Login timeout"})

        user_obj.update_time = now
        user_obj.save()

        return user_obj, user_obj.id


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        token 是一种用户的登录信息
        """
        token = request.META.get("HTTP_TOKEN")
        user_obj = User.objects.filter(token=token)
        if user_obj:
            return user_obj, token
        else:
            raise AuthenticationFailed({"code": 400, "status": 200, "data": "", "message": "Not login"})

    def authenticate_header(self, request):
        return "123"
