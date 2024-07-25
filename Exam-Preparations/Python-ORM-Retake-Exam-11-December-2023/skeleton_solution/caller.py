import datetime
import os
import random
import django

from django.db.models import Q, Count



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
from main_app.choices import TournamentSurfaceTypeChoice

# Create queries within functions

def get_tennis_players(search_name=None, search_country=None) -> str:
    if search_name is None and search_country is None:
        return ''
        
    query = Q()
    
    if search_name is not None:
        query &= Q(full_name__icontains=search_name )
    
    if search_country is not None:
        query &= Q(country__icontains=search_country)
        
    tennis_players = TennisPlayer.objects.filter(query).order_by('ranking')
    
    if not tennis_players:
        return ''
        
    return '\n'.join(
        f'Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}'
        for player in tennis_players
    )


def get_top_tennis_player() -> str:
    top_tennis_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()
    
    if top_tennis_player is None:
        return ''
        
    return f'Top Tennis Player: {top_tennis_player.full_name} with {top_tennis_player.wins_count} wins.'


def get_tennis_player_by_matches_count() -> str:
    tennis_player = TennisPlayer.objects.annotate(
        matches_count=Count('matches')
    ).order_by(
        '-matches_count',
        'ranking'
    ).first()
    
    if tennis_player is None or tennis_player.matches_count == 0:
        return ''
        
    return f'Tennis Player: {tennis_player.full_name} with {tennis_player.matches_count} matches played.'
