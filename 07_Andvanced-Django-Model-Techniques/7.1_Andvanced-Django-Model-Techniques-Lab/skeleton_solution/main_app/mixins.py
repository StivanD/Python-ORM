from django.db import models
from django.core.validators import MaxValueValidator


class ReviewMixin(models.Model):
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    
    class Meta:
        abstract = True
        ordering = ["-rating"]