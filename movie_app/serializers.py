from rest_framework import serializers
from .models import Director, Movie, Review

class DirectorSerializer(serializers.ModelSerializer):
    movie_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Director
        fields = 'id name movie_count'.split()

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Имя режиссера должно быть более 3 символов")
        return value

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director'.split()

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Название фильма должно быть не менее 3 символов.")
        return value

    def validate_descriprion(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Описание фильма должно быть не менее 1 символа.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Продолжительность фильма должна быть положительным числом.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Текст отзыва должен быть не менее 10 символов.")
        return value
