from datetime import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce.models import Transaction, Product

class Review(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True, help_text='Enter a title for the review')
    text = models.TextField(blank=True, null=True, help_text='Enter your review of the product')
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                       help_text='Enter your rate for the product (1-10)')
    date = models.DateField(blank=True, default=datetime.now)

    user = models.ForeignKey(User, on_delete=CASCADE)
    trans = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('trans', 'product'),)
        ordering = ['product', 'date']
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.trans.__str__()

    def get_absolute_url(self):
        return reverse('review-detail', args=[str(self.id)])
