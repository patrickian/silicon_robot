from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import serializers

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.viewsets import (
    GenericViewSet as generic_set
)

from config.utils.send_mail import send_activation_mail
from config.utils.oauth_handler import OAuthHandler
from oauth2_provider.ext.rest_framework import OAuth2Authentication

from api.serializers import (
    UserListSerializer,
    UnauthenticatedUserListSerializer,
    UserSignupSerializer,
    UserLoginSerializer,
)


class UserViewSet(OAuthHandler, generic_set):
    '''
        HANDLER for User functions,
        Inherits OAuthHandler for Auth functions
    '''
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    authenication_classes = [OAuth2Authentication]

    # FOR RESPONSE MESSAGES AND STATUS
    r_text = 'OK'
    r_status = status.HTTP_200_OK

    @list_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def signup(self, request):
        ''' ENDPOINT : /api/users/signup/
        '''
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

    @list_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        ''' ENDPOINT : /api/users/login/
        '''
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

    @list_route(
        methods=['patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def change_password(self, request):
        ''' ENDPOINT : /api/users/change_password/
        '''
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
        ''' ENDPOINT : /api/users/{pk}/activate/
        '''
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

    @list_route(methods=['get'], permission_classes=[permissions.AllowAny])
    def lists(self, request):
        '''
            ENDPOINT : /api/users/lists/
        '''
        if request.auth:
            r_text = self.get_serializer(self.queryset, many=True).data
        else:
            r_text = UnauthenticatedUserListSerializer(
                self.queryset, many=True).data

        r_status = status.HTTP_200_OK
        return Response(r_text, status=r_status)
