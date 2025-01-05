from rest_framework import serializers
from .models import Director, Movie, Review

class DirectorSerializer(serializers.ModelSerializer):
    class Meta: