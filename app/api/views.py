import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import serializers
from django.utils import timezone

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.viewsets import (
    ModelViewSet as model_set
)
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application
from config.utils.send_mail import send_activation_mail
from api.serializers import (
    UserListSerializer,
    UserSignupSerializer,
    UserLoginSerializer,
)


class OAuthHandler:
    def create_application(self, user):
        return Application.objects.create(
            user=user,
            client_type='confidential',
            authorization_grant_type='password',
            name=user.username
        )


    def __create_expiration(self):
        return timezone.now() + timezone.timedelta(days=1)

    def create_token(self, app):
        return AccessToken.objects.create(
            user=app.user,
            application=app,
            expires=self.__create_expiration(),
            token=generate_token()
        )

    def get_user_token(self, user, token=None):
        token_obj = AccessToken.objects.get(user=user)
        if token:
            return token_obj if token == token_obj.token else None
        else:
            return token_obj


    def validate_token(self, token):
        return (
            True if token.expires > timezone.now()
            else False
        )

    def refresh_token(self, user):
        token = self.get_user_token(user)

        if not self.validate_token(token):
            token.token = generate_token()
            token.expires = self.__create_expiration()
            token.save()
        return token
        

class UserViewSet(OAuthHandler, model_set):
    
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    # FOR RESPONSE MESSAGES AND STATUS
    r_text = 'OK'
    r_status = status.HTTP_200_OK

    @list_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def user_signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            app = self.create_application(user)
            token = self.create_token(app)

            r_text = serializer.validated_data
            r_status = status.HTTP_200_OK

            send_activation_mail(token)
        else:
            r_text = serializer.errors
            r_status = status.HTTP_400_BAD_REQUEST

        return Response(r_text, status=r_status)


    @list_route(methods=['post'])
    def user_login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=request.data.get('email'),
                password=request.data.get('password')
            )
            if user and user.is_active:
                token = self.refresh_token(user)
                r_text = token.token
                r_status = status.HTTP_200_OK              
            else:
                r_text = 'Invalid Username/Password'
                r_status = status.HTTP_401_UNAUTHORIZED

        else:
            r_text = serializer.errors
            r_status = status.HTTP_400_BAD_REQUEST


        return Response(r_text, status=r_status)


    @list_route(methods=['patch'])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            request.user.set_password(
                request.data['password']
            )
            request.user.save()
            r_text = 'OK'
            r_status = status.HTTP_200_OK
        else:
            r_text = serializer.errors 
            r_status = status.HTTP_400_BAD_REQUEST


        return Response(r_text, status=r_status)

    @detail_route(methods=['get'], permission_classes=[permissions.AllowAny])
    def activate(self, request, pk=None):
        token = request.query_params.get('temp')
        user = User.objects.get(id=pk)
        is_auth = self.get_user_token(user, token)
        if is_auth and self.validate_token(is_auth):
            user.is_active = True
            user.save()
            r_text = serializers.serialize('json', [user])
            r_status = status.HTTP_200_OK

        else:
            r_text = 'Token Expired/ Wrong Token.'
            r_status = status.HTTP_401_UNAUTHORIZED

        return Response(r_text, status=r_status)
