from ecommerce.models import Transaction, Product
from django.contrib.auth.models import User
from customer.models import Wishlist

def get_nav_count(request):
    if request.user.is_authenticated:
        user_transaction_count = Transaction.objects.filter(customer=request.user,state=Transaction.pending).count()
        user_wishlist_count = (Product.objects.filter(wishlist__user=request.user).count())
        print('yes the user is logged-in')
    else:
        print('no the user is not logged-in')
        user_transaction_count = None
        user_wishlist_count = None

    return {
        'transaction_count':user_transaction_count,
        'wishlist_count':user_wishlist_count,

            }