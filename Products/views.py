from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .pagination import ProductsPagination
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer

class ProductsView(APIView):
    """
    Read-only products API
    - search: ?search=<taom nomi>
    - filter: ?category=<category>
    - pagination: ?page=<number> (14 items per page)
    """
    permission_classes = [permissions.AllowAny]


    def get(self, request):
        products = Product.objects.all().order_by('id')  # SORT ADDED

        # Search
        search_query = request.query_params.get('search')
        if search_query:
            products = products.filter(name__icontains=search_query)

        # Filter
        category_filter = request.query_params.get('category')
        if category_filter:
            products = products.filter(category=category_filter)

        # Pagination
        paginator = ProductsPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
