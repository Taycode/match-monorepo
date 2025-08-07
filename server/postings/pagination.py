from rest_framework.pagination import CursorPagination, PageNumberPagination


class PostingCursorPagination(CursorPagination):
    page_size = 5  # Number of items per page
    ordering = '-created_at'  # Field to order by (must be indexed)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
