from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review, ConfirmationCode
from .serializers import ( DirectorSerializer, MovieSerializer, ReviewSerializer,
                            RegisterSerializer, ConfirmUserSerializer)
from django.db.models import Avg, Count
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class DirectorsListView(APIView):
    def get(self, request):
        directors = Director.objects.annotate(movie_count=Count('movie'))
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DirectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectorDetailView(APIView):
    def get(self, request, id):
        try:
            director = Director.objects.get(id=id)
            serializer = DirectorSerializer(director)
            return Response(serializer.data)
        except Director.DoesNotExist:
            return Response({'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            director = Director.objects.get(id=id)
            serializer = DirectorSerializer(instance=director, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Director.DoesNotExist:
            return Response({'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            director = Director.objects.get(id=id)
            director.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Director.DoesNotExist:
            return Response({'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)


class MoviesListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    def get(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(instance=movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)


class ReviewsListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    def get(self, request, id):
        try:
            review = Review.objects.get(id=id)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            review = Review.objects.get(id=id)
            serializer = ReviewSerializer(instance=review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            review = Review.objects.get(id=id)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
            )
            user.is_active = False
            user.save()

            ConfirmationCode.objects.create(user=user)

            return Response({'message': 'Регистрация успешна. Проверьте код подтверждения.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'error': 'Пользователь не активен'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class ConfirmUserView(APIView):
    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data['username'])
            user.is_active = True
            user.save()
            user.confirmation_code.delete()
            return Response({'message': 'Пользователь успешно подтвержден'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)