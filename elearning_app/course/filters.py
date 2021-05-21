from django_filters import rest_framework as filters
from .models import Course


class CourseFilter(filters.FilterSet):
    is_student = filters.BooleanFilter(method="get_filter_user_courses")

    def get_filter_user_courses(self, queryset, name, value):
        user = getattr(self.request, 'user', None)
        if user.is_anonymous:
            return queryset
        if value:
            queryset = queryset.is_student(user)
        return queryset

    class Meta:
        model = Course
        fields = ['category', 'is_student']
