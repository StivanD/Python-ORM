from django.db import models

from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator

from main_app.mixins import NameMixin, UpdatedAtMixin, LaunchDateMixin
from main_app.choices import MissionStatusChoice
from main_app.managers import AstronautManager


# Create your models here.
class Astronaut(NameMixin, UpdatedAtMixin):
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(regex=r'^\d+$')
        ],
        unique=True
    )
    
    is_active = models.BooleanField(
        default=True
    )
    
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    
    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    objects = AstronautManager()
    
class Spacecraft(NameMixin, UpdatedAtMixin, LaunchDateMixin):
    manufacturer = models.CharField(
        max_length=100
    )
    
    
    capacity = models.SmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    
    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )
    

class Mission(NameMixin, UpdatedAtMixin, LaunchDateMixin):
    description = models.TextField(
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=9,
        choices=MissionStatusChoice.choices,
        default=MissionStatusChoice.PLANNED
    )
    
    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions'
    )
    
    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions'
    )
    
    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        related_name='commanded_missions',
        null=True,
        blank=True  
    )