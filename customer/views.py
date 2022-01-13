from typing import List
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Min
from django.db.models.fields import FloatField
from django.contrib.auth.models import Group
from django.db.models import Sum, F

from .models import Profile, Wishlist
from review.models import Review
from ecommerce.models import Product, Transaction, Key
from .forms import SignUpForm

def add_to_wishlist(request):
    user = request.user
    wishlist_user= Wishlist.objects.get(user=user)

    product_id = request.POST.get("product_id")
    wishlist_user.products.add(product_id)

    return redirect('/customer/wishlist')

def delete_to_wishlist(request):
    user = request.user
    wishlist_user= Wishlist.objects.get(user=user)

    product_id = request.POST.get("product_id")
    wishlist_user.products.remove(product_id)

    return redirect('/customer/wishlist')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = Profile(user=new_user)
            new_profile.save()
            return redirect('/accounts/login/')
    else:
        form = SignUpForm()
    messages.info(request, 'Popo fiero')
    return render(request, 'customer/signup.html', {'form': form})


@register.filter
def round_number(number, decimal_number):
    return round(number, decimal_number)


"""
def user(request):
    try:
        user_id = request.GET.get('id')
        current_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise HttpResponseNotFound("The the product with the ID:"+user_id+" does not exist")

    context = {'user': current_user}
    return render(request, 'customer/profilesettings.html', context)
"""

@login_required
def keymanager(request):
    products=Product.objects.all().order_by("name")

    product_id = request.POST.get("product_name")
    code_key = request.POST.get("code")
    price_key = request.POST.get("price")
    percentage_discount = request.POST.get("time")
    time_discount = request.POST.get("percentage_discount")

    # if request.method == 'POST':
    #     form = AddkeyForm(request.POST)
    #     if form.is_valid():
    #         new_key_form = form.save()
    #         # new_key = Key()
    #         # new_key.save()
    #         return redirect('customer/addkeymanager')



    contex={
        'products':products,
    }
    return render(request,'customer/keymanager.html',contex)


@login_required
def library(request):
    return render(request,'customer/library.html')


@login_required
def wishlist(request):
    user = request.user
    product_list_alphabetic = (Product.objects
                                      .filter(wishlist__user=user)
                                      .annotate(min_price=Min(F('key__price')/(100/(F('key__sale')))), review_count=Count('review')/7, review_rate=Sum('review__rate')/Count('review'))
                                      .order_by('name'))
    product_list_price = (Product.objects.filter(wishlist__user=user)
                                        .annotate(min_price=Min(F('key__price')/(100/(F('key__sale')))), review_count=Count('review')/7, review_rate=Sum('review__rate')/Count('review'))
                                        .order_by('min_price'))

    context = {
        'product_list_alphabetic': product_list_alphabetic,
        'product_count': product_list_alphabetic.count(),
        'product_list_price': product_list_price,
    }
    return render(request,'customer/wishlist.html', context)


@register.filter
def get_key_count(product):
    return Key.objects.filter(product=product, sold=False).count()


@register.filter
def get_key_insale_count(product):
    return Key.objects.filter(product=product, sold=False, sale__gt=0).count()


@login_required
def profilesettings(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('customer/profilesettings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    is_seller = True if user.groups.filter(name='Sellers').exists() else False
    purchased_keys_count = Transaction.objects.filter(state=Transaction.success, seller=user).count()
    review_count = Review.objects.filter(user=user).count()
    seller_keys_avaible = Key.objects.filter(seller=user, sold=False)
    seller_keys_avaible_count = seller_keys_avaible.count()
    seller_sold_keys_count = Key.objects.filter(seller=user, sold=True).count()
    
    contex = {
        'user': user,
        'is_seller': is_seller,
        'purchased_keys_count': purchased_keys_count,
        'review_count': review_count,
        'keys_avaible': seller_keys_avaible,
        'keys_avaible_count': seller_keys_avaible_count,
        'sold_keys_count': seller_sold_keys_count,
        'seller_rate_count': user.profile.seller_ratings_count if user.groups.filter(name='Sellers').exists() else 0,
        'seller_rate': round(user.profile.seller_total_ratings/user.profile.seller_ratings_count, 1) if user.profile.seller_ratings_count!=0 else 0,
        'form': form,
    }
    return render(request,'customer/profilesettings.html',contex)


@login_required
def becomeseller(request):
    user = request.user
    group = Group.objects.get(name='Sellers')
    user.groups.add(group)
    return redirect('/customer/settings')


@login_required
def becomecustomer(request):
    user = request.user
    group = Group.objects.get(name='Sellers')
    user.groups.remove(group)
    return redirect('/customer/settings')

"""
# Testing view
def provaform(request):
    return render(request, 'customer/provaform.html')
"""

def addkeyconfirmation(request):
    product_id=request.POST.get("product_id")
    code_key=request.POST.get("code")
    price_key=request.POST.get("price")
    percentage_discount=request.POST.get("time")
    time_discount=request.POST.get("percentage_discount")
    product=Product.objects.get(id=product_id)

    contex = {
        'product':product,
        'code_key':code_key,
        'price_key':price_key,
        'percentage_discount':percentage_discount,
        'time_discount':time_discount,
    }
    return render(request, 'customer/addkeyconfirmation.html', contex)
