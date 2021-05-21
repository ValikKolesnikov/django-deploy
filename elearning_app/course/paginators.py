from rest_framework.pagination import LimitOffsetPagination


class CoursePaginator(LimitOffsetPagination):
    default_limit = 20
