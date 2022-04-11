from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Max, Min, Count, Sum
from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime
from ecommerce.models import Product, Genre, Key, Transaction
from review.models import Review


@login_required
def cart(request):
    transaction_list = Transaction.objects.filter(customer=request.user, state=Transaction.pending).order_by('-date_time')
    total_real_cost = 0
    total_cost = 0 

    for transaction in transaction_list:
        total_real_cost += transaction.key.sale_price
        total_cost += transaction.key.price

    context = {
        'transaction_list': transaction_list,
        'transaction_count': transaction_list.count(),
        'total_real_cost': round(total_real_cost, 2),
        'total_cost': round(total_cost, 2),
        'payment_method': [Transaction.visa, Transaction.mastercard, Transaction.maestro, Transaction.paypal],
    }

    return render(request, 'ecommerce/cart.html', context)


@login_required
def add_to_cart(request):
    user = request.user
    key_id = request.POST.get("key_id")
    key = Key.objects.get(id=key_id)
    seller_username = request.POST.get("seller_username")
    seller = User.objects.get(username=seller_username)
    new_transaction = Transaction(state=Transaction.pending , key=key,customer=user,seller=seller)
    new_transaction.save()

    return redirect('/cart')


@login_required
def remove_from_cart(request):
    transaction_id = request.POST.get("transaction_id")
    transaction_to_remove = Transaction.objects.filter(id=transaction_id)
    transaction_to_remove.delete()

    return redirect('/cart')


@login_required
def buy_keys(request):
    user = request.user
    pay_method = request.POST.get("pay_method")
    transaction_list = Transaction.objects.filter(customer=user, state=Transaction.pending)
    for transaction in transaction_list:
        key_sold = Key.objects.get(serial_key=transaction.key)
        key_sold.sold = True
        key_sold.save()

        if pay_method == 'Visa':
            transaction.payment_method = Transaction.visa
        elif pay_method == 'MasterCard':
            transaction.payment_method = Transaction.mastercard
        elif pay_method == 'Maestro':
            transaction.payment_method = Transaction.maestro
        elif pay_method == 'PayPal':
            transaction.payment_method = Transaction.paypal

        transaction.date_time = datetime.now()
        transaction.state = Transaction.success
        transaction.save()

    return redirect('/cart')


def product(request):
    product_id = request.GET.get('id')
    keys = Key.objects.filter(product_id=product_id, sold=False).order_by('price')
    keys_count = Key.objects.filter(product_id=product_id, sold=False).order_by('price').count
    current_product = get_object_or_404(Product, pk=product_id)
    # rate product
    current_reviews = Review.objects.filter(product_id=product_id)
    review_count = Review.objects.filter(product_id=product_id).count()
    total_rate = Review.objects.filter(product_id=product_id).aggregate(Sum('rate'))["rate__sum"] or 0
    product_rate = (total_rate / review_count) if review_count != 0 else 0
    context = {
        'product': current_product,
        'keys': keys,
        'keys_count': keys_count,
        'review':current_reviews,
        'review_count':review_count,
        'review_product_rate':total_rate,
        'product_rate':product_rate,
    }

    return render(request, 'ecommerce/product.html', context)


def homepage(request):
    products = Product.objects.annotate(Count('key')).filter(key__count__gt=0, key__sold=False).order_by('-id')[:9]
    newest_product= Product.objects.all().order_by('-publishing_date')[:3]
    context = {
        'product_count': products.count(),
        'product_limit': products,
        'newest_product': newest_product,
    }

    return render(request, 'ecommerce/homepage.html', context)



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

    genres = Genre.objects.all()
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
    product = Product.objects.annotate(Count('key')).filter(key__count__gt=0, key__sold=False).order_by('-id')[:4]
    context = {
                'product_bottom': product,
                'products':products,
                'tab_sale':tab_sale,
                'keys': keys,
                'user': user,
               }

    return render(request, 'ecommerce/scout.html', context)


def search(request):
    q = request.GET.get("q")
    products = Product.objects.filter(name__contains=q).order_by("name")
    products_count = products.count()

    if q == "":
        products_count = 0

    context = {
                'search': q,
                'products': products,
                'products_count': products_count,
    }

    return render(request, 'ecommerce/search.html', context)
