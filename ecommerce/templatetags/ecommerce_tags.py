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
def get_seller_data(user):
    return Key.objects.filter(seller=user, sold=True).count()


@register.filter
def get_best_price(product):
    if Key.objects.filter(product=product, sold=False).order_by('sale_price').count() < 1:
        price = "Out of stock"
        sale_price = price
        sale = 0
    else:
        key_best_price = Key.objects.filter(product=product, sold=False).order_by('sale_price')
        price = key_best_price[0].price
        sale_price = key_best_price[0].sale_price
        sale = key_best_price[0].sale

    return {
        'price': price,
        'sale_price': sale_price,
        'sale': sale,
            }


@register.filter
def get_seller_rate(user):
    return user.profile.seller_total_ratings/user.profile.seller_ratings_count if user.profile.seller_ratings_count>0 else "No ratings"
