from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'main_category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get products by category"""
        category = request.GET.get('category', '')
        if category:
            products = Product.objects.filter(category=category, is_active=True)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search products"""
        query = request.GET.get('q', '')
        if query:
            products = Product.objects.filter(
                name__icontains=query,
                is_active=True
            )[:20]
            serializer = self.get_serializer(products, many=True)
            return Response({
                'query': query,
                'count': products.count(),
                'results': serializer.data
            })
        return Response({'query': '', 'count': 0, 'results': []})
    
    @action(detail=False, methods=['get'])
    def supplements(self, request):
        """Get all supplements"""
        supplements = Product.objects.filter(category='SUP', is_active=True)
        serializer = self.get_serializer(supplements, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for categories (read-only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for orders (authenticated users only)
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductStatsAPIView(APIView):
    """
    API endpoint for product statistics
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        total_products = Product.objects.filter(is_active=True).count()
        total_supplements = Product.objects.filter(category='SUP', is_active=True).count()
        total_clothing = Product.objects.filter(category='CLO', is_active=True).count()
        total_equipment = Product.objects.filter(category='EQU', is_active=True).count()
        total_food = Product.objects.filter(category='FOO', is_active=True).count()
        
        # Get average price
        from django.db.models import Avg, Max, Min
        price_stats = Product.objects.filter(is_active=True).aggregate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            min_price=Min('price')
        )
        
        return Response({
            'total_products': total_products,
            'by_category': {
                'supplements': total_supplements,
                'clothing': total_clothing,
                'equipment': total_equipment,
                'food': total_food,
            },
            'price_statistics': price_stats
        })