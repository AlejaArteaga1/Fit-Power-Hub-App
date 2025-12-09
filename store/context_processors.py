from .utils import get_or_create_cart

def cart_items_count(request):
    """
    Add cart items count to all templates
    """
    cart_items_count = 0
    if request.user.is_authenticated or request.session.session_key:
        try:
            cart = get_or_create_cart(request)
            cart_items_count = cart.total_items
        except:
            pass
    
    return {'cart_items_count': cart_items_count}