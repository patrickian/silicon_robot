from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.viewsets import (
    ModelViewSet as model_set
)

from api.serializers import UserListSerializer


class UserViewSet(model_set):
    
    queryset = User.objects.all()
    serializer_class = UserListSerializer


    @list_route()
    def user_list(self):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
