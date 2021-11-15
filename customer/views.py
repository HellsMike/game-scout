import logging

from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
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