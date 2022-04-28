from ecommerce.models import Transaction, Product
from django.contrib.auth.models import User
from customer.models import Wishlist


def get_seller_state(request):
    user = request.user
    is_seller = False

    if user.is_authenticated:
        is_seller = True if user.groups.filter(name='Sellers').exists() else False
        
    return {
        'seller_state': is_seller,
    }


def get_nav_count(request):
    user_transaction_count = None
    user_wishlist_count = None

    if request.user.is_authenticated:
        user_transaction_count = Transaction.objects.filter(customer=request.user,state=Transaction.pending).count()
        user_wishlist_count = Product.objects.filter(wishlist__user=request.user).count()

    return {
        'transaction_count': user_transaction_count,
        'wishlist_count': user_wishlist_count,
            }