from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Max, Min, Count, Sum
from django.shortcuts import redirect, render, get_object_or_404

from customer.models import Wishlist
from ecommerce.models import Product, Genre, Key, Transaction
from django.template.defaulttags import register

from review.models import Review

@login_required
def add_to_cart(request):
    user = request.user

    product_id = request.POST.get("product_id")
    key_id=request.POST.get("key_id")
    key=Key.objects.get(id=key_id)
    seller_username=request.POST.get("seller_username")
    seller=User.objects.get(username=seller_username)

    new_transaction= Transaction(state=Transaction.pending , key=key,customer=user,seller=seller)
    new_transaction.save()

    return redirect('/cart')

@login_required
def remove_to_cart(request):
    user = request.user

    transaction_id = request.POST.get("transaction_id")
    transaction_to_remove = Transaction.objects.filter(id=transaction_id)
    transaction_to_remove.delete()

    return redirect('/cart')

@login_required
def buy_keys(request):
    user = request.user
    pay_method=request.POST.get("pay_method")
    transaction_list=Transaction.objects.filter(customer=user, state=Transaction.pending)
    for transaction in transaction_list:
        transaction.state=Transaction.success
        key_sold=Key.objects.get(serial_key=transaction.key)
        key_sold.sold = True
        key_sold.save()
        if pay_method == 'Visa':
            transaction.payment_method= Transaction.visa
            print("1")
            print(pay_method)
        elif pay_method == 'MasterCard':
            transaction.payment_method = Transaction.mastercard
            print("2")
            print(pay_method)
        elif pay_method == 'Maestro':
            transaction.payment_method = Transaction.maestro
            print("3")
            print(pay_method)
        elif pay_method == 'PayPal':
            transaction.payment_method = Transaction.paypal
            print("4")
            print(pay_method)
        transaction.save()

    return redirect('/cart')



@register.filter
def get_name_product(key):
    product_name = Product.objects.get(key=key)
    return product_name

@register.filter
def get_id_product(key):
    product_name = Product.objects.get(key=key)
    return product_name.id

@register.filter
def get_total_rate(key):
    product_id = get_id_product(key)
    total_rate = Review.objects.filter(product_id=product_id).aggregate(Sum('rate'))["rate__sum"] or 0
    review_count = Review.objects.filter(product_id=product_id).count()
    product_rate = (total_rate / review_count) if review_count != 0 else 0
    return product_rate

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

@register.filter
def get_best_price(product):
    if Key.objects.filter(product=product, sold=False).order_by('price').count()==0:
        best_price="out of stock"
    else:
        key_best_price = Key.objects.filter(product=product, sold=False).order_by('price')
        best_price = key_best_price[0].price
    return best_price


@register.filter
def get_key_sale(transaction):
    key = Key.objects.get(serial_key=transaction)
    return key.sale

@register.filter
def get_key_price_by_transaction(transaction):
    key = Key.objects.get(serial_key=transaction)
    return key.price

@register.filter
def get_best_sale(product):
    if Key.objects.filter(product=product, sold=False).order_by('price').count() == 0:
        best_sale =0
    else:
        key_best_sale = Key.objects.filter(product=product, sold=False).order_by('-sale','price')
        best_sale=key_best_sale[0].sale

    return best_sale

@register.filter
def get_count_key_by_product_id(product):
    product_count = Key.objects.filter(product=product, sold=False).count()
    return product_count

# @login_required
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

    # seller=user.groups.filter(name='Sellers')

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
    product = Product.objects.annotate(Count('key')).filter(key__count__gt=0, key__sold=False).order_by('-id')[:4]

    context = {
                'product_bottom': product,
                'products':products,
                'tab_sale':tab_sale,
                'keys': keys,
                'user': user,
               }
    return render(request,'ecommerce/scout.html',context)

def search(request):
    q=request.GET.get("q")
    products=Product.objects.filter(name__contains=q).order_by("name")
    products_count=products.count()

    context = {
                'search':q,
                'products':products,
                'products_count':products_count,
    }
    return render(request, 'ecommerce/search.html',context)