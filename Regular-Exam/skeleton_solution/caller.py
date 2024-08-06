import os
import django

from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from main_app.choices import MissionStatusChoice

# Create queries within functions
def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ''

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(
            phone_number__icontains=search_string)
    )

    astronauts = astronauts.order_by('name')

    if not astronauts.exists():
        return ''

    result = []

    for astronaut in astronauts:
        status = 'Active' if astronaut.is_active else 'Inactive'
        result.append(f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {status}")

    return '\n'.join(result)


def get_top_astronaut() -> str:
    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not top_astronaut or top_astronaut.missions_count == 0:
        return 'No data.'

    return f'Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions.'


def get_top_commander() -> str:
    top_commander = Astronaut.objects.annotate(
        missions_count=Count('commanded_missions')
    ).filter(
        missions_count__gt=0
    ).order_by(
        '-missions_count',
        'phone_number'
    ).first()

    if not top_commander:
        return "No data."

    return f'Top Commander: {top_commander.name} with {top_commander.missions_count} commanded missions.'


def get_last_completed_mission() -> str:
    last_completed_mission = Mission.objects.filter(
        status=MissionStatusChoice.COMPLETED
    ).select_related(
        'spacecraft',
        'commander'
    ).prefetch_related(
        'astronauts'
    ).order_by(
        '-launch_date'
    ).first()
    
    if not last_completed_mission:
        return 'No data.'

    commander_name = last_completed_mission.commander.name if last_completed_mission.commander else 'TBA'
    
    astronaut_names = ', '.join(last_completed_mission.astronauts.order_by('name').values_list('name', flat=True))
    
    total_spacewalks = last_completed_mission.astronauts.aggregate(total_spacewalks=Sum('spacewalks'))['total_spacewalks'] or 0
    
    return (f'The last completed mission is: {last_completed_mission.name}. '
            f'Commander: {commander_name}. Astronauts: {astronaut_names}. '
            f'Spacecraft: {last_completed_mission.spacecraft.name}. '
            f'Total spacewalks: {total_spacewalks}.')


def get_most_used_spacecraft() -> str:
    most_used_spacecraft = Spacecraft.objects.annotate(
        missions_count=Count('missions')
    ).order_by(
        '-missions_count',
        'name'
    ).first()
    
    if not most_used_spacecraft or most_used_spacecraft.missions_count == 0:
        return 'No data.'
    
    unique_astronauts_count = Mission.objects.filter(
        spacecraft=most_used_spacecraft
    ).values_list(
        'astronauts', flat=True
    ).distinct().count()
    
    return (f'The most used spacecraft is: {most_used_spacecraft.name}, '
            f'manufactured by {most_used_spacecraft.manufacturer}, '
            f'used in {most_used_spacecraft.missions_count} missions, '
            f'astronauts on missions: {unique_astronauts_count}.')
    

def decrease_spacecrafts_weight() -> str:
    spacecrafts = Spacecraft.objects.filter(
        missions__status=MissionStatusChoice.PLANNED,
        weight__gte=200.0
    ).distinct()
    
    if not spacecrafts.exists():
        return 'No changes in weight.'
    
    affected_spacecrafts_count = spacecrafts.count()
    
    spacecrafts.update(weight=F('weight') - 200.0)
    
    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight'] or 0.0
    
    return f'The weight of {affected_spacecrafts_count} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg'