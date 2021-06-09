from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Category
from .paginators import CoursePaginator
from .serializers import CourseListResponseSerializer, CategorySerializer, CourseSerializer
from .filters import CourseFilter
from .permission import IsAdminOrReadOnly
from .services import enroll_as_student
from .tasks import create_random_courses


class CourseViewSet(viewsets.GenericViewSet):
    pagination_class = CoursePaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        queryset = Course.objects.published().prefetch_related('lessons').attach_number_of_steps()
        if user and not user.is_anonymous:
            queryset = queryset.attach_number_of_completed_steps(user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseListResponseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CourseListResponseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = CourseSerializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def create_random_course_num(self, request):
        create_random_courses.delay(1000)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def enroll_as_student(self, request, pk=None):
        course = self.get_object()
        user = request.user
        enroll_as_student(user=user, course=course)
        return Response(status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer
