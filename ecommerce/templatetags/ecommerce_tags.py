from django import template
from django.db.models import Sum
from ecommerce.models import Key
from review.models import Review


register = template.Library()


@register.filter
def get_total_rate(product):
    review_count = Review.objects.filter(product_id=product.id).count()
    product_rate = 0

    if review_count > 0:
        total_rate = Review.objects.filter(product_id=product.id).aggregate(Sum('rate'))["rate__sum"] or 0
        product_rate = (total_rate / review_count)

    return product_rate


@register.filter
def get_rate_count(product):
    return Review.objects.filter(product_id=product.id).count()


@register.filter
def is_seller(user):
    return True if user.groups.filter(name='Sellers').exists() else False


@register.filter
def is_admin(user):
    return True if user.groups.filter(name='Admins').exists() else False


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def extract_price(keys, index):
    return keys[index].price


@register.filter
def get_seller_data(user):
    return Key.objects.filter(seller=user, sold=True).count()


@register.filter
def get_best_price(product):
    if Key.objects.filter(product=product, sold=False).order_by('price').count() < 1:
        best_price = "Non disponibile"
    else:
        key_best_price = Key.objects.filter(product=product, sold=False).order_by('price')
        best_price = key_best_price[0].price
        best_sale = key_best_price[0].sale

    return {'best_price': best_price,
            'best_sale': best_sale,}


@register.filter
def get_seller_rate(user):
    return user.profile.seller_total_ratings/user.profile.seller_ratings_count if user.profile.seller_ratings_count>0 else "Nessusa valutazione"
