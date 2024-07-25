import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Q, Count

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


def get_tournaments_by_surface_type(surface=None) -> str:
    if surface is None:
        return ''
        
    tournaments = Tournament.objects.prefetch_related(
        'matches'
    ).annotate(
        num_matches=Count('matches')
    ).filter(
        surface_type__icontains=surface
    ).order_by(
        '-start_date'
    )
    
    if not tournaments:
        return ''
    
    return '\n'.join(
        f'Tournament: {tournament_info.name}, start date: {tournament_info.start_date}, matches: {tournament_info.num_matches}'
        for tournament_info in tournaments
    )
    
def get_latest_match_info() -> str:
    latest_match = Match.objects.prefetch_related(
        'players'
    ).order_by(
        '-date_played',
        '-id'
    ).first()
    
    if latest_match is None:
        return ''
    
    players = latest_match.players.order_by('full_name')
    player1_full_name = players.first().full_name
    player2_full_name = players.last().full_name
    winner_full_name = 'TBA' if latest_match.winner is None else latest_match.winner.full_name
    
    return f'Latest match played on: {latest_match.date_played}, tournament: {latest_match.tournament.name}, ' \
           f'score: {latest_match.score}, players: {player1_full_name} vs {player2_full_name}, ' \
           f'winner: {winner_full_name}, summary: {latest_match.summary}'


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return 'No matches found.'
        
    matches = Match.objects.select_related(
        'tournament',
        'winner'
    ).filter(
        tournament__name__exact=tournament_name
    ).order_by(
        '-date_played'
    )
    
    if not matches:
        return 'No matches found.'
        
    return '\n'.join(
        f'Match played on: {match.date_played}, score: {match.score}, winner: {match.winner.full_name if match.winner else "TBA"}'
        for match in matches
    )

