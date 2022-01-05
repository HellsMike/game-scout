import logging

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import SignUpForm

# Create your views here.
def signup(request):
    """
    if request.method == 'GET':
        return render(request, 'customer/signup.html')
    elif request.method == 'POST':
        logging.warning('Email: ' + request.POST['email'])

        if(request.POST['password'] != request.POST['password_confirmation']):
            messages.error(request, 'username or password not correct')
            return render(request, 'customer/signup.html')
        try:
            user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
            user.save()
        except():
            return render(request, 'customer/signup.html')
    return render(request, 'accounts/login.html')
"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.save()
            return redirect('/accounts/login/')
    else:
        form = SignUpForm()
    return render(request, 'customer/signup.html', {'form': form})

def user(request):
    try:
        user_id = request.GET.get('id')
        current_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("The the product with the ID:"+user_id+" does not exist")

    context = {'user': current_user}
    return render(request, 'customer/profilesettings.html', context)

def keymanager(request):
    return render(request,'customer/keymanager.html')

def library(request):
    return render(request,'customer/library.html')

def wishlist(request):
    return render(request,'customer/wishlist.html')

def profilesettings(request):
    return render(request,'customer/profilesettings.html')

def provaform(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False) # Don't save it yet
            new_review.save()
            return redirect('/accounts/login/')
    else:
        form = SignUpForm()
    return render(request, 'customer/provaform.html', {'form': form})

