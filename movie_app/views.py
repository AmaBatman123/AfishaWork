from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from django.db.models import Avg, Count

@api_view(http_method_names=['GET', 'POST'])
def directors_list(request):
    if request.method == 'GET':
        directors = Director.objects.annotate(movie_count=Count('movie'))
        if not directors:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'Directors not found'})

        data_directors = DirectorSerializer(instance=directors, many=True).data
        return Response(data_directors)
    elif request.method == 'POST':
        pass

@api_view(http_method_names=['GET'])
def detail_director_view(request, id):
    director = Director.objects.get(id=id)
    data = DirectorSerializer(instance=director).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def movies_list(request):
    try:
        movies = Movie.objects.all()
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Movies not found'})

    data_movies = MovieSerializer(instance=movies, many=True).data
    return Response(data_movies)

@api_view(http_method_names=['GET'])
def detail_movie_view(request, id):
    movie = Movie.objects.get(id=id)
    data = MovieSerializer(instance=movie).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def reviews_list(request):
    try:
        reviews = Review.objects.all()
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Reviews not found'})

    data_reviews = ReviewSerializer(instance=reviews, many=True).data
    return Response(data_reviews)

@api_view(http_method_names=['GET'])
def detail_review_view(request, id):
    review = Review.objects.get(id=id)
    data = ReviewSerializer(instance=review).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def movies_with_reviews_list(request):
    movies = Movie.objects.all()
    data_movies = []

    for movie in movies:
        reviews = movie.review_set.all()
        avg_rating = reviews.aggregate(Avg('stars'))['stars__avg']
        data_review = ReviewSerializer(instance=reviews, many=True).data

        data_movies.append({
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'duration': movie.duration,
            'director': movie.director.name,
            'reviews': data_review,
            'rating': avg_rating if avg_rating else 0
        })

    return Response(data=data_movies)

