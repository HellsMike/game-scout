from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Profile
from review.models import Review
from ecommerce.models import Transaction, Key
from .forms import SignUpForm


# Create your views here.
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


def user(request):
    try:
        user_id = request.GET.get('id')
        current_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise HttpResponseNotFound("The the product with the ID:"+user_id+" does not exist")

    context = {'user': current_user}
    return render(request, 'customer/profilesettings.html', context)


def keymanager(request):
    return render(request,'customer/keymanager.html')


def library(request):
    return render(request,'customer/library.html')


def wishlist(request):
    return render(request,'customer/wishlist.html')


def profilesettings(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('/accounts/login/')

    is_seller = True if user.groups.filter(name='Sellers').exists() else False
    purchased_keys_count = Transaction.objects.filter(state=Transaction.success).count()
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
        'seller_rate': user.profile.seller_total_ratings/user.profile.seller_ratings_count if user.profile.seller_ratings_count!=0 else 0,
    }
    return render(request,'customer/profilesettings.html',contex)


# Testing view
def provaform(request):
    return render(request, 'customer/provaform.html')

