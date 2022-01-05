from django.core.paginator import Paginator
from django.db.models import Max, Min, Count
from django.http import Http404
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from customer.models import Profile
from ecommerce.models import Product, Genre, Key
from django.template.defaulttags import register

# @login_required
def product(request):
    try:
        product_id = request.GET.get('id')
        keys = Key.objects.filter(product_id=product_id).order_by('price')
        #print(keys[0].price)
        current_product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("The the product with the ID:" + product_id + " does not exist")

    context = {'product': current_product,
               'keys': keys
               }
    return render(request, 'ecommerce/product.html', context)


def homepage(request):


    return render(request, 'ecommerce/homepage.html')


def cart(request):
    return render(request,'ecommerce/cart.html')


# set catalog filter:
#   best sale on product filter,
#   best price on product filter,
# set Paginator object and product are rendered in a page

def catalog(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    genreId = request.GET.get('genre')

    products = Product.objects.all().annotate(Count('key')).filter(key__count__gt=0, key__sold=False)

    if genreId:
        genre = Genre.objects.get(id=genreId)
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
        'selectedGenre': genreId,
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
