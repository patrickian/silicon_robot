from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.viewsets import (
    ModelViewSet as model_set
)

from api.serializers import (
    UserListSerializer,
    UserSignupSerializer,
    UserLoginSerializer,
)


class UserViewSet(model_set):
    
    queryset = User.objects.all()
    serializer_class = UserListSerializer


    @list_route(methods=['post','get'])
    def user_signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer = serializer.validated_data
        else:
            serializer = serializer.errors

        return Response(serializer)


    @list_route(methods=['post'])
    def user_login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        r_text = 'OK'
        r_status = status.HTTP_200_OK

        if serializer.is_valid():
            user = authenticate(
                username=request.data.get('email'),
                password=request.data.get('password')
            )
            if user and user.is_active:
                pass
            else:
                r_text = 'Invalid Username/Password'
                r_status = status.HTTP_401_UNAUTHORIZED

        else:
            r_text = 'Invalid Username/Password'
            r_status = status.HTTP_401_UNAUTHORIZED


        return Response(r_text, status=r_status)
