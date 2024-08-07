from django.db import models

from django.core.validators import MinLengthValidator


class ContentMixin(models.Model):
    
    class Meta:
        abstract = True
        
        
    content = models.TextField(
            validators=[
                MinLengthValidator(10)
            ]
        )
    

class PublishedOnMixin(models.Model):
    
    class Meta:
        abstract = True
        
        
    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )