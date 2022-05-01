from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from ecommerce.models import Product, Transaction
from .models import Review
from .forms import ReviewForm


@register.filter
def get_review(reviews, index):
    return reviews[index].text


def review(request, prod_id):
    current_product = Product.objects.get(id=prod_id)
    is_bought = Transaction.objects.filter(customer=request.user, key__product__id=prod_id, state=Transaction.success).exists()
    user_review = Review.objects.filter(product_id=prod_id, user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False) # Don't save it yet
            new_review.product = current_product # Add product
            transaction = Transaction.objects.filter(customer=request.user, key__product__id=prod_id).order_by('-date_time').first()
            new_review.trans = transaction
            new_review.user = request.user
            new_review.save()
            return redirect(f'/review/{prod_id}')
    else:
        try:
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
        'is_bought': is_bought,
        'user_review': user_review,
        'reviews': current_reviews,
        'number_review': review_count,
        'rate_count': rate_count,
        'product_rate': product_rate,
        'product': current_product,
        'form': form,
    }
    return render(request, 'review/review.html', context)


@login_required
def remove_review(request):
    review_id = request.POST.get("review_id")
    review_to_remove = Review.objects.filter(id=review_id)
    review_to_remove.delete()

    return redirect(f'/review/{request.POST.get("prod_id")}')
