from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from main_app.choices import ZooKeeperSpecialtyChoice
# Create your models here.


class Animal(models.Model):
    name = models.CharField(
        max_length=100
    )

    species = models.CharField(
        max_length=100
    )

    birth_date = models.DateField()

    sound = models.CharField(
        max_length=100
    )
    
    @property
    def age(self):
        current_date = date.today()
        
        return current_date.year - self.birth_date.year - ((current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day))


class Mammal(Animal):
    fur_color = models.CharField(
        max_length=50
    )


class Bird(Animal):
    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )


class Reptile(Animal):
    scale_type = models.CharField(
        max_length=50
    )


class Employee(models.Model):
    class Meta:
        abstract = True
        
    first_name = models.CharField(
        max_length=50
    )
    
    last_name = models.CharField(
        max_length=50
    )
    
    phone_number = models.CharField(
        max_length=10
    )
    

class ZooKeeper(Employee):
    specialty = models.CharField(
        max_length=10,
        choices=ZooKeeperSpecialtyChoice.choices
    )
    
    managed_animals = models.ManyToManyField(
        to=Animal
    )
    
    def clean(self):
        if (self.specialty, self.specialty) not in ZooKeeperSpecialtyChoice.choices:
            raise ValidationError("Specialty must be a valid choice.")


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = (
            (True, "Available"),
            (False, "Not Available")
        )
        
        kwargs["default"] = True
        
        super().__init__(*args, **kwargs)
        

class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10
    )
    
    availability = BooleanChoiceField()
    
    def is_available(self):
        return self.availability


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True
        
    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."
    
    def is_endangered(self):
        if self.species in ["Cross River Gorilla", "Orangutan", "Green Turtle"]:
            return f"{self.species} is at risk!"
        
        return f"{self.species} is not at risk."