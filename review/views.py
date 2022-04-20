from django.db.models import Sum
from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from ecommerce.models import Product
from .models import Review
from .forms import ReviewForm


@register.filter
def get_review(reviews, index):
    return reviews[index].text


def review(request, prod_id):
    if request.method == 'POST':
        prod_id = request.POST.get('id')
        print(prod_id)
        product = get_object_or_404(Product, pk=prod_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False) # Don't save it yet
            new_review.product = product # Add product
            new_review.save()
            return redirect('/wwww')
    else:
        try:
            current_product = Product.objects.get(pk=prod_id)
            base_query = Review.objects.filter(product_id=prod_id)
            current_reviews = base_query.exclude(title__isnull=True).order_by('-date')
            review_count = current_reviews.count()
            rate_count = base_query.count()
            total_rate = base_query.aggregate(Sum('rate'))["rate__sum"] or 0
            product_rate = (total_rate / rate_count) if rate_count != 0 else 0
            form = ReviewForm()
        except Product.DoesNotExist:
            return HttpResponseNotFound("The the product with the ID:" + prod_id + " does not exist") 

    context = {
        'reviews': current_reviews,
        'number_review': review_count,
        'rate_count': rate_count,
        'product_rate': product_rate,
        'product': current_product,
        'user': request.user,
        'form': form,
    }
    return render(request, 'review/review.html', context)
