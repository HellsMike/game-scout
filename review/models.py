from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

import ecommerce.models


class Review(models.Model):
    # id = models.BigAutoField(primary_key=True)
    trans = models.OneToOneField(ecommerce.models.Transaction, on_delete=models.SET_NULL, null=True)
    # customer
    product = models.ForeignKey(ecommerce.models.Product, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64, blank=True, null=True, help_text='Enter a title for the review')
    text = models.TextField(blank=True, null=True, help_text='Enter your review of the product')
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                       help_text='Enter your rate for the product (1-10)')
    date = models.DateField()

    class Meta:
        unique_together = (('trans', 'product'),)
        ordering = ['product', 'date']
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('review-detail', args=[str(self.id)])
