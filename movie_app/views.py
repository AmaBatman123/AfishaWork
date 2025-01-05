from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

@api_view(http_method_names=['GET', 'POST'])
def directors_list(request):
    if request.method == 'GET':
        directors = Director.objects.all()
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
    movies = Movie.objects.all()
    data_movies = MovieSerializer(instance=movies, many=True).data
    return Response(data_movies)

@api_view(http_method_names=['GET'])
def detail_movie_view(request, id):
    movie = Movie.objects.get(id=id)
    data = MovieSerializer(instance=movie).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def reviews_list(request):
    reviews = Review.objects.all()
    data_reviews = ReviewSerializer(instance=reviews, many=True).data
    return Response(data_reviews)

@api_view(http_method_names=['GET'])
def detail_review_view(request, id):
    review = Review.objects.get(id=id)
    data = ReviewSerializer(instance=review).data
    return Response(data=data)

