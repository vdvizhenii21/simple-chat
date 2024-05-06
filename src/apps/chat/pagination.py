from rest_framework.pagination import LimitOffsetPagination


class PaginationThread(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class PaginationMessages(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100
