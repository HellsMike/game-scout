from background_task import background
from ecommerce.models import Transaction


@background(schedule=3600)
def t_remove_from_cart(trans_id):
    trans_to_remove = Transaction.objects.filter(id=trans_id)
    if trans_to_remove.state == Transaction.pending:
        trans_to_remove.delete()
