from django.db import models

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

from main_app.choices import TournamentSurfaceTypeChoice
from main_app.managers import TennisPlayerManager

# Create your models here.
class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(5)
        ]
    )
    
    birth_date = models.DateField()
    
    country = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ]
    )
    
    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(150)
        ]
    )
    
    is_active = models.BooleanField(
        default=True
    )
    
    objects = TennisPlayerManager()
    

class Tournament(models.Model):
    name = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(2)
        ],
        unique=True
    )
    
    location = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ]
    )
    
    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    start_date = models.DateField()
    
    surface_type = models.CharField(
        max_length=12,
        choices=TournamentSurfaceTypeChoice.choices,
        default=TournamentSurfaceTypeChoice.NOT_SELECTED
    )
    

class Match(models.Model):
    class Meta:
        verbose_name_plural = 'Matches'
        
        
    score = models.CharField(
        max_length=100
    )
    
    summary = models.TextField(
        validators=[
            MinLengthValidator(5)
        ]
    )
    
    date_played = models.DateTimeField()
    
    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    
    players = models.ManyToManyField(
        to=TennisPlayer,
        related_name='matches'
    )
    
    winner = models.ForeignKey(
        to=TennisPlayer,
        on_delete=models.SET_NULL,
        related_name='matches_won',
        null=True,
        blank=True
    )