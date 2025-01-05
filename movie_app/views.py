from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review

@api_view(http_method_names=['GET', 'POST'])
def directors_list(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data_directors = [
            {
                "id": director.id,
                "name": director.name
            }
            for director in directors
        ]
        return Response(data_directors)
    elif request.method == 'POST':
        pass


@api_view(http_method_names=['GET'])
def movies_list(request):
    movies = Movie.objects.all()
    data_movies = [
        {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "duration": movie.duration,
            "director": movie.director.name,

        }
        for movie in movies
    ]
    return Response(data_movies)

@api_view(http_method_names=['GET'])
def reviews_list(request):
    reviews = Review.objects.all()
    data_reviews = [
        {
            "id": review.id,
            "text": review.text,
            "movie": review.movie.title,
        }
        for review in reviews
    ]
    return Response(data_reviews)

