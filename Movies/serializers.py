from rest_framework import serializers
from .models import Genre, Movie, Review, Comment, Profile

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genres', 'release_year', 'director', 'description', 'poster_image']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'rating', 'content', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'review', 'username', 'user', 'content', 'created_at']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar']
