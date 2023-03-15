from rest_framework.pagination import PageNumberPagination


class PaginatorLimit(PageNumberPagination):
    def get_page_size(self, request):
        limit = request.query_params.get("limit")
        if limit:
            return limit
        return 5
