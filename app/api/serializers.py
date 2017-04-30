from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator

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
        required=True
    )
    email = serializers.EmailField(
        max_length=128,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
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
            last_name=validated_data.get('last_name') or '',
            is_active=False
        )



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=128,
        required=True,
    )
    password = serializers.CharField(
        max_length=512,
        required=True
    )

    class Meta:
        model = User
        fields = ('email', 'password')
