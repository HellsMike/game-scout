from django.http import Http404
from django.shortcuts import render

# Create your views here.
from ecommerce.models import Product


def product(request):
    try:
        product_id = request.GET.get('id')
        current_product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("The the product with the ID:"+product_id+" does not exist")

    context = {'product': current_product}
    return render(request, 'ecommerce/product.html', context)
