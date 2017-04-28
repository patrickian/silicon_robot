from django.contrib.auth.models import User

from rest_framework import serializers

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'is_active',
        )
