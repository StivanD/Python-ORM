from django.db import models


class MissionStatusChoice(models.TextChoices):
    PLANNED = 'Planned', 'Planned'
    ONGOING = 'Ongoing', 'Ongoing'
    COMPLETED = 'Completed', 'Completed'