from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import ProductViewSet, CategoryViewSet, OrderViewSet, ProductStatsAPIView

# Create router for API
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # API Endpoints
    path('api/', include([
        path('', include(router.urls)),
        path('stats/', ProductStatsAPIView.as_view(), name='api_stats'),
        path('demo/', views.api_demo_view, name='api_demo'),
    ])),
    
    # Product Views
    path('', views.product_list_view, name='product_list'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    
    # Cart Views
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Order Views
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:order_id>/', views.order_summary_view, name='order_summary'),
    path('orders/', views.order_history_view, name='order_history'),
    
    # Profile View
    path('profile/', views.profile_view, name='profile'),
]