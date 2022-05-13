from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce'

    def ready(self):
        from .tasks import t_remove_expired_sale
        from background_task.models import Task

        background_tasks = Task.objects.filter(task_name='ecommerce.tasks.t_remove_expired_sale')

        for background_task in background_tasks:
            background_task.delete()
            
        t_remove_expired_sale(repeat=3600)
