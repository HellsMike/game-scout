from ecommerce.models import Transaction
from customer.models import Wishlist

def get_nav_count(request):
    # user_transaction_count = Transaction.object.filter(customer=request.user)
    # print(user_transaction_count)
    mes="ciao"

    return {'mes':mes}