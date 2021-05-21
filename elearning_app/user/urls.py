from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TokenObtainView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('token/obtain/', TokenObtainView.as_view())
]
