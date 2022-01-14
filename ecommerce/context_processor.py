from ecommerce.models import Transaction
from customer.models import Wishlist

def get_nav_count(request):
    user_transaction_count = Transaction.object
    mes="ciao"

    return {'mes':mes}