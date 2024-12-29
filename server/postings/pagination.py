from rest_framework.pagination import CursorPagination


class PostingCursorPagination(CursorPagination):
    page_size = 10  # Number of items per page
    ordering = '-created_at'  # Field to order by (must be indexed)
