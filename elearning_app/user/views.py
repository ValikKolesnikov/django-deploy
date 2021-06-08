from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .serializers import UserResponseSerializer, UserRequestSerializer, TokenObtainRequestSerializer, \
    TokenObtainResponseSerializer, UserUpdateRequestSerializer, ResetPasswordSerializer, \
    ResetPasswordConfirmSerializer
from .models import User
from .services import update_user, send_reset_password_email
from .permissions import AdminOrIsOwnerPermission
from .paginators import UserPaginator


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [AdminOrIsOwnerPermission]
    pagination_class = UserPaginator

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserResponseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserResponseSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        refresh_token = RefreshToken.for_user(user)
        response_data = {'token': str(refresh_token.access_token),
                         'user': user}
        response_serializer = TokenObtainResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserResponseSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateRequestSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        update_user(user=user, **serializer.validated_data)
        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def current(self, request):
        user = request.user
        serializer = UserResponseSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data['email'])
        send_reset_password_email(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenObtainView(APIView):
    def post(self, request):
        serializer = TokenObtainRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh_token = RefreshToken.for_user(user)
        response_data = {'token': str(refresh_token.access_token),
                         'user': user}
        response_serializer = TokenObtainResponseSerializer(response_data)
        return Response(response_serializer.data)
