from ecommerce.models import Transaction, Product
from django.contrib.auth.models import User
from customer.models import Wishlist

def get_nav_count(request):
    user_transaction_count = Transaction.objects.filter(customer=request.user,state=Transaction.pending).count()
    user_wishlist_count = (Product.objects.filter(wishlist__user=request.user).count())

    return {
        'transaction_count':user_transaction_count,
        'wishlist_count':user_wishlist_count,

            }