from background_task import background
from ecommerce.models import Transaction


@background(schedule=1800)
def t_remove_from_cart(trans_id):
    trans_to_remove = Transaction.objects.filter(id=trans_id).first()
    if trans_to_remove:
        if trans_to_remove.state == Transaction.pending:
            trans_to_remove.delete()
            print(f'Transacion #{trans_id} removed')
