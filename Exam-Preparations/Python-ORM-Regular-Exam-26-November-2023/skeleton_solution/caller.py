import os
import django

from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author

# Create queries within functions
def get_authors(search_name=None, search_email=None) -> str:
    if search_name is None and search_email is None:
        return ''
        
    query = Q()
    if search_name is not None:
        query &= Q(full_name__icontains=search_name)
    if search_email is not None:
        query &= Q(email__icontains=search_email)
        
    authors = Author.objects.filter(query).order_by('-full_name')
    
    if not authors.exists():
        return ''
        
    result = []
    
    for author in authors:
        status = 'Banned' if author.is_banned else 'Not Banned'
        result.append(f'Author: {author.full_name}, email: {author.email}, status: {status}')
    
    return '\n'.join(result)


def get_top_publisher() -> str:
    top_publisher = Author.objects.get_authors_by_article_count().first()
    
    if top_publisher is None or top_publisher.article_count == 0:
        return ''
        
    return f'Top Author: {top_publisher.full_name} with {top_publisher.article_count} published articles.'
    

def get_top_reviewer() -> str:
    top_reviewer = Author.objects.annotate(
        reviews_count=Count('reviews')
    ).order_by(
        '-reviews_count',
        'email'
    ).first()
    
    if top_reviewer is None or top_reviewer.reviews_count == 0:
        return ''
    
    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews.'
