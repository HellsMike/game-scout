from django.http import Http404
from django.shortcuts import render
from django.template.defaulttags import register

# Create your views here.
from ecommerce.models import Product
from review.models import Review

@register.filter
def get_review(reviews, index):
    return reviews[index].text


def review(request):
    try:
        product_id = request.GET.get('id')
        current_product = Product.objects.get(pk=product_id)

        current_reviews = Review.objects.filter(product_id=product_id).order_by('date')
        reviewproduct= Review.objects.filter(product_id=product_id).count()

    except Product.DoesNotExist:
        raise Http404("The the product with the ID:" + product_id + " does not exist")

    context = {
        'reviews':current_reviews,
        'reviewsprova':current_reviews[0].title,
        'reviewstext':current_reviews[0].text,
        'numberreview':reviewproduct,
        'product':current_product,
    }
    print(current_reviews[0].text)
    print(current_reviews[0].title)
    print(current_reviews[0].rate)
    return render(request,'review/review.html',context)
