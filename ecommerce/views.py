from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Max, Min, Count, Sum
from django.shortcuts import redirect, render, get_object_or_404
from ecommerce.models import Product, Genre, Key, Transaction
from django.template.defaulttags import register

from review.models import Review

@login_required
def add_to_cart(request):
    user = request.user

    product_id = request.POST.get("product_id")
    serial_key=request.POST.get("serial_key")
    key=Key.objects.filter(serial_key=serial_key)
    seller_username=request.POST.get("seller_username")
    seller=User.objects.filter(username=seller_username)

    new_transaction= Transaction(state=Transaction.pending,key=key[0],customer=user,seller=seller[0])
    new_transaction.save()

    return redirect('/cart')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def extract_price(keys, index):
    return keys[index].price

@register.filter
def round_number(number, decimal_number):
    return round(number, decimal_number)

@register.filter
def get_seller_data(user):
    seller_sold_keys_count = Key.objects.filter(seller=user, sold=True).count()
    return seller_sold_keys_count

# @login_required
def product(request):
    product_id = request.GET.get('id')
    keys = Key.objects.filter(product_id=product_id, sold=False).order_by('price')
    current_product = get_object_or_404(Product, pk=product_id)

    # rate product
    current_reviews = Review.objects.filter(product_id=product_id)
    review_count = Review.objects.filter(product_id=product_id).count()
    total_rate = Review.objects.filter(product_id=product_id).aggregate(Sum('rate'))["rate__sum"] or 0
    product_rate = (total_rate / review_count) if review_count != 0 else 0

    # seller=user.groups.filter(name='Sellers')

    context = {
        'product': current_product,
        'keys': keys,
        'review':current_reviews,
        'review_count':review_count,
        'review_product_rate':total_rate,
        'product_rate':product_rate,
    }
    return render(request, 'ecommerce/product.html', context)


def homepage(request):
    tab_sale = [0, 1, 2]

    context={
        'tab_sale':tab_sale,
    }
    return render(request, 'ecommerce/homepage.html',context)


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
    user = request.user
    products=Product.objects.filter().order_by('id')
    keys = Key.objects.filter().order_by('price','sale')
    tab_sale=[0,1,2]
    context = {
                'products':products,
                'tab_sale':tab_sale,
                'keys': keys,
                'user': user,
               }
    return render(request,'ecommerce/scout.html',context)

def search(request):
    q=request.GET.get("q")
    products=Product.objects.filter(name__contains=q).order_by("name")

    context = {
                'search':q,
                'products':products,
    }
    return render(request, 'ecommerce/search.html',context)