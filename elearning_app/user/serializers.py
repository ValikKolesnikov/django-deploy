from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import User
from .services import decode_uid


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_teacher']


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_teacher']


class UserUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_teacher']

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        uid = decode_uid(data['uid'])
        user = get_object_or_404(User, pk=uid)
        if not user:
            raise serializers.ValidationError('invalid uid')
        is_token_valid = default_token_generator.check_token(user, data['token'])
        if not is_token_valid:
            raise serializers.ValidationError('invalid token')
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('passwords do not match')
        data['user'] = user
        return data

class TokenObtainRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('No active user found with the given credential')
        return user


class TokenObtainResponseSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    user = UserResponseSerializer()
