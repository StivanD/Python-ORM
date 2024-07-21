from django.db import models

class MovieGenreChoice(models.TextChoices):
    ACTION = "Action", "Action"
    COMEDY = "Comedy", "Comedy"
    DRAMA = "Drama", "Drama"
    OTHER = "Other", "Other"
