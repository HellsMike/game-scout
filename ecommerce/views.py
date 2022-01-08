from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Max, Min, Count
from django.shortcuts import render, get_object_or_404
from ecommerce.models import Product, Genre, Key, Transaction
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def extract_price(keys, index):
    return keys[index].price


# @login_required
def product(request):
    product_id = request.GET.get('id')
    keys = Key.objects.filter(product_id=product_id).order_by('price')
    current_product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': current_product,
        'keys': keys
    }
    return render(request, 'ecommerce/product.html', context)


def homepage(request):
    return render(request, 'ecommerce/homepage.html')


@login_required
def cart(request):
    user = request.user
    product_list = Transaction.objects.filter(customer=user, state=Transaction.pending).order_by('-date_time')
    context = {
        'product_list': product_list,
        'product_count': product_list.count(),
        'payment_method': [Transaction.visa, Transaction.mastercard, Transaction.maestro, Transaction.paypal],
    }
    return render(request,'ecommerce/cart.html', context)


# set catalog filter:
#   best sale on product filter,
#   best price on product filter,
# set Paginator object and product are rendered in a page

def catalog(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    genre_id = request.GET.get('genre')
    products = Product.objects.annotate(Count('key')).filter(key__count__gt=0, key__sold=False)

    if genre_id:
        genre = Genre.objects.get(id=genre_id)
        products = products.filter(genre=genre)

    paged = Paginator(products, int(limit))
    page_results = paged.page(page).object_list
    sales = dict()
    prices = dict()

    # Ciclo tutti i prodotti nella pagina corrente
    for product in page_results:
        maxSaleSet = Key.objects.filter(product_id=product.id, sold=False).aggregate(Max('sale'))
        minPrice = Key.objects.filter(product_id=product.id, sold=False).aggregate(Min('price'))
        prices[product.id] = minPrice['price__min']
        if maxSaleSet["sale__max"] is not None:
            sales[product.id] = maxSaleSet['sale__max']

    genres = Genre.objects.all()[:11]
    context = {
        'results': page_results,
        'currentPage': page,
        'totalPages': paged.num_pages,
        'totalItems': paged.count,
        'pageRange': paged.page_range,
        'limit': int(limit),
        'genres': genres,
        'selectedGenre': genre_id,
        'availableLimits': [10, 20, 30, 40, 50],
        'sales': sales,
        'prices': prices,
    }

    return render(request, 'ecommerce/catalog.html', context)


def scout(request):
    # product_id = request.GET.get('id')
    # keys = Key.objects.filter(product_id=product_id).order_by('price')
    # # print(keys[0].price)
    # current_product = Product.objects.get(pk=product_id)
    #
    # context = {'product': current_product,
    #            'keys': keys
    #            }
    return render(request,'ecommerce/scout.html')
