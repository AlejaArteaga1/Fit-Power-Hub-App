from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart, CartItem, Order, OrderItem, UserProfile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create user profile when new user is created
    """
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f"Profile created for user: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save user profile when user is saved
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Order)
def update_product_stock(sender, instance, created, **kwargs):
    """
    Update product stock when order is delivered
    """
    if instance.status == 'DEL' and not created:
        for order_item in instance.items.all():
            product = order_item.product
            product.stock -= order_item.quantity
            if product.stock < 0:
                product.stock = 0
            product.save()
            logger.info(f"Stock updated for product: {product.name}")