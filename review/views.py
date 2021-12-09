from django.shortcuts import render

# Create your views here.
from review.models import Review


def review(request):
    # review = Review.object.all()
    return render(request,'review/review.html')
