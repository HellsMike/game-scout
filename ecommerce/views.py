from django.http import Http404
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from customer.models import Profile
from ecommerce.models import Product


# @login_required
def product(request):
    try:
        product_id = request.GET.get('id')
        current_product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("The the product with the ID:"+product_id+" does not exist")

    context = {'product': current_product}
    return render(request, 'ecommerce/product.html', context)


def homepage(request):

    context = {}

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context = {'profile': profile}

    return render(request, 'ecommerce/homepage.html', context)
