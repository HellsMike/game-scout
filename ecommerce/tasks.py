from django.utils import timezone
from datetime import datetime
from background_task import background
from ecommerce.models import Transaction, Key


@background(schedule=1800)
def t_remove_from_cart(trans_id):
    try:
        trans_to_remove = Transaction.objects.get(id=trans_id)
    except Transaction.DoesNotExist:
        print(f'[{datetime.now}] Transaction #{trans_id} doesn\'t exist anymore')
        trans_to_remove = None

    if trans_to_remove:
        if trans_to_remove.state == Transaction.pending:
            trans_to_remove.delete()
            print(f'[{datetime.now()}] Transaction #{trans_id} removed')


@background
def t_remove_expired_sale():
    print(f'[{datetime.now()}] Checking for expired sales')
    key_list = Key.objects.filter(sold=False, sale__gt=0, sale_expiry_date__isnull=False)

    for key in key_list:
        if key.sale_expiry_date < timezone.now():
            key.sale = 0
            key.sale_price = key.price
            key.save()

    print(f'[{datetime.now()}] Checked and removed expired sales')
