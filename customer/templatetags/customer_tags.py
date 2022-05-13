from django import template
from ecommerce.models import Key


register = template.Library()


@register.filter
def get_key_count(product):
    return Key.objects.filter(product=product, sold=False).count()


@register.filter
def get_key_sale_count(product):
    return Key.objects.filter(product=product, sold=False, sale__gt=0).count()


@register.filter
def get_max_sale(product):
    sale = Key.objects.filter(product=product, sold=False, sale__gt=0).order_by('-sale').values('sale').first()
    return sale['sale'] if sale!=None else 0


@register.filter
def get_key_insale_count(product):
    return Key.objects.filter(product=product, sold=False, sale__gt=0).count()
