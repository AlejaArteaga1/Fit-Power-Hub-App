from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product, Cart, CartItem, Order, OrderItem, Category, UserProfile
from .forms import ProductForm, CheckoutForm, UserProfileForm
from .utils import get_or_create_cart

def home_view(request):
    """Home page view"""
    try:
        featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
        supplements = Product.objects.filter(category='SUP', is_active=True)[:3]
        equipment = Product.objects.filter(category='EQU', is_active=True)[:3]
        
        context = {
            'featured_products': featured_products,
            'supplements': supplements,
            'equipment': equipment,
        }
    except Exception as e:
        print(f"Error in home_view: {e}")
        context = {}
    
    return render(request, 'store/home.html', context)

def product_list_view(request):
    """Product listing view"""
    category_filter = request.GET.get('category', '')
    type_filter = request.GET.get('type', '')  # Filter by product category (SUP, CLO, EQU, FOO)
    search_query = request.GET.get('q', '')
    
    # Local products
    local_products = Product.objects.filter(is_active=True)
    
    # Filter by main category (Category model)
    if category_filter:
        local_products = local_products.filter(main_category__slug=category_filter)
    
    # Filter by product type (SUP, CLO, EQU, FOO)
    if type_filter:
        local_products = local_products.filter(category=type_filter)
    
    # Filter by search
    if search_query:
        local_products = local_products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': local_products,
        'categories': Category.objects.all(),
        'search_query': search_query,
        'current_category': category_filter,
        'current_type': type_filter,
    }
    
    return render(request, 'store/product_list.html', context)

def product_detail_view(request, product_id):
    """Product detail view"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Get recommended products (same category)
    recommended = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'recommended_products': recommended,
    }
    
    return render(request, 'store/product_detail.html', context)

def cart_view(request):
    """Shopping cart view"""
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.all()
    }
    return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id, is_active=True)
            quantity = int(request.POST.get('quantity', 1))
            
            cart = get_or_create_cart(request)
            
            # Check stock
            if product.stock < quantity:
                messages.error(request, f'Insufficient stock. Only {product.stock} units available.')
                return redirect('product_detail', product_id=product_id)
            
            # Add or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            messages.success(request, f'✅ {product.name} added to cart!')
            
        except Exception as e:
            messages.error(request, 'Error adding to cart')
    
    return redirect('product_detail', product_id=product_id)

def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart=get_or_create_cart(request))
            action = request.POST.get('action')
            
            if action == 'update':
                quantity = int(request.POST.get('quantity', 1))
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            elif action == 'remove':
                cart_item.delete()
            
            cart = get_or_create_cart(request)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'cart_total': cart.total_items,
                    'cart_total_price': float(cart.total_price),
                    'item_total_price': float(cart_item.total_price) if hasattr(cart_item, 'total_price') else 0
                })
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('cart')

@login_required
def checkout_view(request):
    """Checkout process"""
    cart = get_or_create_cart(request)
    
    if cart.items.count() == 0:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.total_price,
                    shipping_address=form.cleaned_data['shipping_address'],
                    billing_address=form.cleaned_data['billing_address'],
                    notes=form.cleaned_data['notes']
                )
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                
                # Clear cart
                cart.items.all().delete()
                
                messages.success(request, f'✅ Order #{order.order_number} placed successfully!')
                return redirect('order_summary', order_id=order.id)
                
            except Exception as e:
                messages.error(request, f'Error processing order: {str(e)}')
    else:
        # Try to pre-fill with user profile data
        try:
            profile = request.user.profile
            initial_data = {
                'shipping_address': profile.address,
                'billing_address': profile.address,
            }
        except UserProfile.DoesNotExist:
            initial_data = {}
        
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'store/checkout.html', context)

@login_required
def order_summary_view(request, order_id):
    """Order summary view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    return render(request, 'store/order_summary.html', context)

@login_required
def order_history_view(request):
    """Order history view"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'store/order_history.html', context)

@login_required
def profile_view(request):
    """User profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'orders': Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    }
    return render(request, 'store/profile.html', context)

def api_demo_view(request):
    """API demo page"""
    return render(request, 'store/api_demo.html')