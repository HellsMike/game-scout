from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import ecommerce.models


class Review(models.Model):
    id_rev = models.UUIDField(unique=True)
    trans = models.ForeignKey(ecommerce.models.Transaction, on_delete=models.SET_NULL)
    text = models.TextField(blank=True, null=True)
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        verbose_name_plural = 'Reviews'
        unique_together = (('id_rev', 'trans'),)
