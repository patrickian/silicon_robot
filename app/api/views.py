from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.viewsets import (
    ModelViewSet as model_set
)

from api.serializers import (
    UserListSerializer,
    UserSignupSerializer,
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
        pass
