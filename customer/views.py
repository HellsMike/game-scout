from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Profile
from review.models import Review
from ecommerce.models import Transaction, Key
from .forms import SignUpForm


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
    return render(request, 'customer/signup.html', {'form': form})

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
    return render(request,'customer/keymanager.html')


@login_required
def library(request):
    return render(request,'customer/library.html')


@login_required
def wishlist(request):
    user = request.user
    product_list = Transaction.objects.filter(customer=user, state=Transaction.pending).order_by('-date_time')
    context = {
        'product_list': product_list,
        'product_count': product_list.count(),
        'payment_method': [Transaction.visa, Transaction.mastercard, Transaction.maestro, Transaction.paypal],
    }
    return render(request,'customer/wishlist.html', context)


@login_required
def profilesettings(request):
    user = request.user
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

