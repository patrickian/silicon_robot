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


class UserSignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=512,
        write_only=True,
        required=True
    )
    email = serializers.EmailField(
        max_length=30,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'password',
            'email',
        )

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name') or '',
            last_name=validated_data.get('last_name') or ''
        )
