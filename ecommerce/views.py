from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.db.models import Max, Count, Sum, Q, FloatField
from django.db.models.functions import Cast
from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime
from background_task.models import Task
from ecommerce.forms import AddProductForm
from ecommerce.models import Category, Developer, Product, Genre, Key, Publisher, Transaction
from ecommerce.tasks import t_remove_from_cart
from gs.settings import EMAIL_HOST_USER
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
    key_id = request.POST.get('key_id')
    
    if(key_id != ''):
        key = Key.objects.get(id=key_id)
    else:
        product_id = request.POST.get('product_id')
        key = Key.objects.filter(product__id=product_id).order_by('sale_price').first()
    
    if(key):
        seller = User.objects.get(username=key.seller)
        
        try:
            new_transaction = Transaction(state=Transaction.pending , key=key, customer=user, seller=seller)
            new_transaction.save()
            t_remove_from_cart(new_transaction.id)
        except IntegrityError:
            return redirect(f'/product/{key.product.id}')

    return redirect('/cart')


@login_required
def remove_from_cart(request):
    transaction_id = request.POST.get("transaction_id")
    transaction_to_remove = Transaction.objects.filter(id=transaction_id)
    transaction_to_remove.delete()
    task_parms = '[[' + transaction_id + '], {}]'
    task_to_remove = Task.objects.get(task_params=task_parms)
    task_to_remove.delete()

    return redirect('/cart')


@login_required
def buy_keys(request):
    user = request.user
    pay_method = request.POST.get("pay_method")
    transaction_list = Transaction.objects.filter(customer=user, state=Transaction.pending)
    email_text = 'You bought these products from our site:\n\n'

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
        email_text += f'€{key_sold.sale_price}   {key_sold.product}\n'
    
    if transaction_list.exists():
        email_text += '\nLeave a review on GameScout!'
        try:
            send_mail('Your order on GameScout', email_text, EMAIL_HOST_USER, [user.email])
        except:
            print('Email not sent')

    return redirect('/cart')


def product(request, id):
    keys = Key.objects.filter(product_id=id, sold=False).exclude(transaction__state=Transaction.pending).order_by('sale_price')
    current_product = get_object_or_404(Product, pk=id)
    reviews_q = Review.objects.filter(product_id=id)
    rate_count = reviews_q.count()
    current_reviews = reviews_q.exclude(title__isnull=True)
    review_count = current_reviews.count()
    total_rate = reviews_q.aggregate(Sum('rate'))["rate__sum"] or 0
    product_rate = total_rate / review_count if review_count != 0 else 0
    context = {
        'product': current_product,
        'keys': keys,
        'keys_count': keys.count(),
        'rate_count': rate_count,
        'review_count': review_count,
        'review_product_rate': total_rate,
        'product_rate': product_rate,
    }

    return render(request, 'ecommerce/product.html', context)


def homepage(request):
    products = Product.objects.annotate(Count('key')).filter(key__sold=False, key__count__gt=0)
    most_sold = products.filter(key__transaction__state=Transaction.success).annotate(Count('key__transaction')).order_by('-key__transaction__count')[:3]
    big_sales = products.annotate(Max('key__sale')).filter(key__sale__max__gt=0).order_by('-key__sale__max')[:10]
    lastests = products.order_by('-publishing_date')[:10]
    top_rated = products.annotate(product_rate=(Cast(Sum('review__rate'), FloatField())/Cast(Count('review'), FloatField()))).order_by('-product_rate')[:10]
    context = {
        'most_sold_list': most_sold,
        'big_sales_list': big_sales,
        'lastests_list': lastests,
        'top_rated_list': top_rated,
    }

    return render(request, 'ecommerce/homepage.html', context)


def catalog(request, limit, page, gen):
    products = Product.objects.annotate(Count('key')).filter(key__sold=False, key__count__gt=0).order_by('name')
    genre = None

    if gen:
        genre = Genre.objects.get(name=gen)
        products = products.filter(genre=genre)

    paginator = Paginator(products, limit)
    current_page = paginator.get_page(page)
    genres = Genre.objects.all()
    context = {
        'current_page': current_page,
        'paginator': paginator,
        'limit': limit,
        'genres': genres,
        'selected_genre': genre,
        'available_limits': [10, 20, 30, 40, 50],
        'not_first_page': current_page.has_previous(),
        'not_last_page': current_page.has_next(),
    }

    return render(request, 'ecommerce/catalog.html', context)


@login_required
def scout(request):
    user = request.user
    relevant_genres = Genre.objects.filter(product__key__transaction__customer=user, product__key__transaction__state=Transaction.success).annotate(intensity=Count('product')).order_by('-intensity')[:3]
    base_q = Product.objects.exclude(key__transaction__customer=user).alias(Count('key'))
    intrested_prod_q = base_q.filter(key__count__gt=0, genre__in=relevant_genres)
    most_sold_intrested_products = intrested_prod_q.annotate(key_sold=Count('key__transaction', filter=Q(key__transaction__state=Transaction.success))).order_by('-key_sold')[:5]
    not_intrested_prod_q = base_q.filter(key__count__gt=0).exclude(genre__in=relevant_genres)
    not_intrested_most_sold = not_intrested_prod_q.annotate(key_sold=Count('key__transaction', filter=Q(key__transaction__state=Transaction.success))).order_by('-key_sold')[:12]
    context = {
                'intrest_most_sold': most_sold_intrested_products,
                'not_intrest_most_sold': not_intrested_most_sold, 
               }

    return render(request, 'ecommerce/scout.html', context)


def search(request):
    q = request.GET.get('q')
    products = Product.objects.filter(name__contains=q).order_by('name')
    context = {
                'search': q,
                'products': products,
                'products_count': products.count() if products != None else 0,
    }

    return render(request, 'ecommerce/search.html', context)


def product_add(request):
    if request.method == 'POST':
        post = request.POST.copy()
        post['publisher'] = Publisher.objects.get_or_create(name=post['publisher'])[0].id
        post['developer'] = Developer.objects.get_or_create(name=post['developer'])[0].id
        post['category'] = Category.objects.get_or_create(name=post['category'])[0].id
        post['genre'] = Genre.objects.get_or_create(name=post['genre'])[0].id
        form = AddProductForm(post, request.FILES)

        if form.is_valid():
            product = form.save()

            return redirect(f'/product/{product.id}')
    else:
        form = AddProductForm()

    publishers = Publisher.objects.all().order_by('name')
    developers = Developer.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    genres = Genre.objects.all().order_by('name')
    context = {
        'form': form,
        'publishers': publishers,
        'developers': developers,
        'categories': categories,
        'genres': genres,
    }

    return render(request, 'ecommerce/product_add.html', context)
