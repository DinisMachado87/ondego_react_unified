from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import User
from rest_framework import status
from .settings import (
    JWT_AUTH_COOKIE,
    JWT_AUTH_REFRESH_COOKIE,
    JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)


@api_view()
def root_route(request):
    return Response({"message": "Welcome to ondego app API!"})


@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        try:
            # Decode the token
            UntypedToken(token)
        except InvalidToken:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Perform additional user validation checks
        user_id = UntypedToken(token).payload.get('user_id')
        user = User.objects.get(id=user_id)

        if not user.is_active:
            return Response({"detail": "User account is disabled."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)
