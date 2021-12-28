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
        review_count = Review.objects.filter(product_id=product_id).count()
        total_rate = Review.objects.filter(product_id=product_id).aggregate(Sum('rate'))
    except Product.DoesNotExist:
        raise Http404("The the product with the ID:" + product_id + " does not exist")

    context = {
        'reviews': current_reviews,
        'numberreview': review_count,
        'product_rate': total_rate/review_conut,
        'product': current_product,
    }
    return render(request,'review/review.html',context)
