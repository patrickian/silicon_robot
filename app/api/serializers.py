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
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
