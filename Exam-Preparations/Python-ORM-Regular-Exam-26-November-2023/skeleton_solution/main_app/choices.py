from django.db import models


class ArticleCategoryChoice(models.TextChoices):
    TECHNOLOGY = 'Technology', 'Technology'
    SCIENCE = 'Science', 'Science'
    EDUCATION = 'Education', 'Education'
