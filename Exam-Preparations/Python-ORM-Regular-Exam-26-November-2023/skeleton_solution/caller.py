from django.db.models import Q, Count, Avg
from main_app.models import Article, Author, Review
import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

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


def get_latest_article() -> str:
    latest_article = Article.objects.prefetch_related(
        'authors',
        'reviews'
    ).order_by(
        '-published_on'
    ).first()

    if latest_article is None:
        return ''

    authors_names = ', '.join(
        author.full_name
        for author in latest_article.authors.all().order_by('full_name')
    )
    reviews_count = latest_article.reviews.count()
    avg_rating = sum([r.rating for r in latest_article.reviews.all()]
                     ) / reviews_count if reviews_count else 0.0

    return f"The latest article is: {latest_article.title}. Authors: {authors_names}. Reviewed: {reviews_count} times." \
        f" Average Rating: {avg_rating:.2f}."


def get_top_rated_article() -> str:
    top_rated_article = Article.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by(
        '-avg_rating',
        'title'
    ).first()

    num_reviews = top_rated_article.reviews.count() if top_rated_article else 0

    if top_rated_article is None or num_reviews == 0:
        return ''

    avg_rating = top_rated_article.avg_rating or 0.0

    return f'The top-rated article is: {top_rated_article.title}, with an average rating of {avg_rating:.2f}, reviewed {num_reviews} times.'


def ban_author(email=None) -> str:
    author = Author.objects.prefetch_related(
        'reviews'
    ).filter(
        email__exact=email
    ).first()

    if email is None or author is None:
        return 'No authors banned.'

    num_reviews_deleted = author.reviews.count()

    author.is_banned = True
    author.save()
    author.reviews.all().delete()

    return f'Author: {author.full_name} is banned! {num_reviews_deleted} reviews deleted.'

