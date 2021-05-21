from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))
]
