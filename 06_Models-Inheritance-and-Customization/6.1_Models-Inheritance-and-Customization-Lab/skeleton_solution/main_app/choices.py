from django.db import models

class ZooKeeperSpecialtyChoice(models.TextChoices):
    MAMMALS = "Mammals", "Mammals"
    BIRDS = "Birds", "Birds"
    REPTILES = "Reptiles", "Reptiles"
    OTHERS = "Others", "Others"