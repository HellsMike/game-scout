from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.db.models.aggregates import Min
from .models import Profile, Wishlist
from review.models import Review
from ecommerce.models import Product, Transaction, Key
from .forms import SignUpForm, AddKeyForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()

            if(new_user.username == 'Admin'):
                new_user.is_staff = True
                new_user.is_superuser = True
                group = Group.objects.get_or_create(name='Admins')[0]
                new_user.groups.add(group)
                new_user.save()

            new_profile = Profile(user=new_user)
            new_profile.save()
            new_wishlist = Wishlist(user=new_user)
            new_wishlist.save()
            login(request, authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1']))
            
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'customer/signup.html', {'form': form})


@login_required
def wishlist(request):
    user = request.user
    product_list_alphabetic = Product.objects.filter(wishlist__user=user).annotate(lowest_price=Min('key__sale_price')).order_by('name')
    product_list_price = Product.objects.filter(wishlist__user=user).annotate(lowest_price=Min('key__sale_price')).order_by('key__sale_price')
    context = {
        'product_list_alphabetic': product_list_alphabetic,
        'product_list_price': product_list_price,
        'product_count': product_list_alphabetic.count(),
    }

    return render(request, 'customer/wishlist.html', context)


@login_required
def add_to_wishlist(request):
    user = request.user
    wishlist_user = Wishlist.objects.get(user=user)
    product_id = request.POST.get("product_id")
    wishlist_user.products.add(product_id)

    return redirect('/wishlist')


@login_required
def remove_from_wishlist(request):
    user = request.user
    wishlist_user = Wishlist.objects.get(user=user)
    product_id = request.POST.get("product_id")
    wishlist_user.products.remove(product_id)

    return redirect('/wishlist')


@login_required
def keymanager(request):
    products = Product.objects.all().order_by("name")
    keys = Key.objects.filter(seller=request.user)
    context = {
        'products': products,
        'keys': keys,
        'keys_count': keys.count(),
    }
    
    return render(request, 'customer/keymanager.html', context)


@login_required
def add_key(request):
    if request.method == 'POST':
        post = request.POST.copy()
        post['product'] = Product.objects.get(name=post['product']).id

        if post['sale'] == '':
            post.pop('sale')

        form = AddKeyForm(post)

        if form.is_valid():
            key_instance = form.save(commit=False)
            key_instance.sale_price = key_instance.price-((key_instance.price/100)*key_instance.sale) if key_instance.sale>0 else key_instance.price
            key_instance.save()
    else:
        form = AddKeyForm()

    return redirect('/keymanager')


@login_required
def sold_key(request):
    key_id=request.POST.get('key_id_to_sell')
    key_sold = Key.objects.get(id=key_id)

    if key_sold.sold == False:
        key_sold.sold = True

    return redirect('/library')


@login_required
def delete_key_by_seller(request):
    key_id = request.POST.get('key_id_to_delete')
    key_to_delete = Key.objects.get(id=key_id)

    if key_to_delete.sold == False:
        key_to_delete.delete()

    return redirect('/keymanager')


@login_required
def modify_key(request):
    key_id = request.POST.get('choose_key_modify')
    key_to_modify = Key.objects.get(id=key_id)
    key_to_modify.serial_key = request.POST.get('serial_key')
    key_to_modify.price = request.POST.get('price')
    key_to_modify.sale = request.POST.get('sale')

    if request.POST.get('sale_expiry_date') != '':
        key_to_modify.sale_expiry_date = request.POST.get('sale_expiry_date')
    
    print(type(key_to_modify.price))
    print(type(key_to_modify.sale))
    key_to_modify.sale_price = float(key_to_modify.price)-(float(key_to_modify.price)/100)*float(key_to_modify.sale)
    key_to_modify.save()

    return redirect('/keymanager')


@login_required
def library(request):
    transactions = Transaction.objects.filter(customer=request.user, state=Transaction.success).order_by('date_time')
    context = {
        'transactions': transactions,
        'transactions_count': transactions.count(),
    }

    return render(request, 'customer/library.html', context)


@login_required
def profilesettings(request):
    user = request.user
    
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/settings')
    else:
        form = PasswordChangeForm(user)
    
    is_seller = True if user.groups.filter(name='Sellers').exists() else False
    purchased_keys_count = Transaction.objects.filter(state=Transaction.success, seller=user).count()
    review_count = Review.objects.filter(user=user).count()
    seller_keys_avaible = Key.objects.filter(seller=user, sold=False)
    seller_sold_keys_count = Key.objects.filter(seller=user, sold=True).count()
    
    while True:
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            new_profile = Profile(user=user)
            new_profile.save()
            continue
        break
    
    context = {
        'user': user,
        'is_seller': is_seller,
        'purchased_keys_count': purchased_keys_count,
        'review_count': review_count,
        'keys_avaible': seller_keys_avaible,
        'keys_avaible_count': seller_keys_avaible.count(),
        'sold_keys_count': seller_sold_keys_count,
        'seller_rate_count': profile.seller_ratings_count if user.groups.filter(name='Sellers').exists() else 0,
        'seller_rate': round(profile.seller_total_ratings/profile.seller_ratings_count, 1) if profile.seller_ratings_count!=0 else 0,
        'form': form,
    }

    return render(request, 'customer/profilesettings.html', context)


@login_required
def becomeseller(request):
    user = request.user
    group = Group.objects.get_or_create(name='Sellers')[0]
    user.groups.add(group)

    return redirect('/settings')


@login_required
def becomecustomer(request):
    user = request.user
    group = Group.objects.get_or_create(name='Sellers')[0]
    user.groups.remove(group)
    keys = Key.objects.filter(seller=user, sold=False)
    for key in keys:
        key.delete()

    return redirect('/settings')


@login_required
def change_pro_pic(request):
    user = request.user
    user_pro_pic = Profile.objects.get(user=user)
    user_pro_pic.picture = request.FILES.get('picture')
    user_pro_pic.save()

    return redirect('/settings')


@login_required
def add_seller_rate(request):
    transaction = Transaction.objects.get(id=request.POST.get('transaction_id'))
    rate = request.POST.get('rate')
    seller = Profile.objects.get(user=transaction.seller)
    transaction.is_seller_rated = True
    seller.seller_ratings_count += 1
    seller.seller_total_ratings += int(rate)
    transaction.save()
    seller.save()
    return redirect('/library')
