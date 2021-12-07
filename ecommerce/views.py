from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from customer.models import Profile
from ecommerce.models import Product, Genre


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

def cart(request):
    return render('ecommerce/cart.html')

def catalog(request):
<<<<<<< HEAD
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    genreId = request.GET.get('genre')

    products = Product.objects.all()

    if genreId:
        genre = Genre.objects.get(id=genreId)
        products = products.filter(genre=genre)

    paged = Paginator(products, int(limit))

    genres = Genre.objects.all()[:11]

    context = {
        'results': paged.page(page).object_list,
        'currentPage': page,
        'totalPages': paged.num_pages,
        'totalItems': paged.count,
        'pageRange': paged.page_range,
        'limit': limit,
        'genres': genres
    }

    return render(request, 'ecommerce/catalog.html', context)
=======
    return render('ecommerce/catalog.html')
>>>>>>> main

def review(request):
    return render('ecommerce/review.html')