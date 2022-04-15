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


def review(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        print(product_id)
        product = get_object_or_404(Product, pk=product_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False) # Don't save it yet
            new_review.product = product # Add product
            new_review.save()
            return redirect('/wwww')
    else:
        try:
            product_id = request.GET.get('id')
            current_product = Product.objects.get(pk=product_id)
            current_reviews = Review.objects.filter(product_id=product_id).order_by('date')
            review_count = Review.objects.filter(product_id=product_id).count()
            total_rate = Review.objects.filter(product_id=product_id).aggregate(Sum('rate'))["rate__sum"] or 0
            product_rate = (total_rate / review_count) if review_count != 0 else 0
            form = ReviewForm()
        except Product.DoesNotExist:
            return HttpResponseNotFound("The the product with the ID:" + product_id + " does not exist") 
    context = {
        'reviews': current_reviews,
        'number_review': review_count,
        'product_rate': product_rate,
        'product': current_product,
        'form': form,
    }
    return render(request, 'review/review.html', context)
