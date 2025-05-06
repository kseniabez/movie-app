from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from Movies.models import Genre, Movie, Review, Comment
from Movies.serializers import GenreSerializer, MovieSerializer, ReviewSerializer, CommentSerializer, ProfileSerializer


class SerializerTestCase(APITestCase):

    def setUp(self):
        self.genre1 = Genre.objects.create(name='Action')
        self.genre2 = Genre.objects.create(name='Drama')

        self.user = User.objects.create_user(username='testuser', password='password')

        self.movie = Movie.objects.create(
            title='Test Movie',
            release_year=2025,
            director='Test Director',
            description='A test movie.',
            poster_image='/posters/4.jpg',
        )
        self.movie.genres.add(self.genre1, self.genre2)

        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=5,
            content='Great movie!',
        )

        self.comment = Comment.objects.create(
            review=self.review,
            user=self.user,
            content='Amazing!',
        )

        self.profile = self.user.profile

    def test_genre_serializer(self):
        genre_data = {'id': self.genre1.id, 'name': self.genre1.name}
        serializer = GenreSerializer(self.genre1)
        self.assertEqual(serializer.data, genre_data)

    def test_movie_serializer(self):
        movie_data = {
            'id': self.movie.id,
            'title': self.movie.title,
            'genres': [{'id': self.genre1.id, 'name': self.genre1.name},
                       {'id': self.genre2.id, 'name': self.genre2.name}],
            'release_year': self.movie.release_year,
            'director': self.movie.director,
            'description': self.movie.description,
            'poster_image': self.movie.poster_image,
        }
        serializer = MovieSerializer(self.movie)
        self.assertEqual(serializer.data, movie_data)

    def test_review_serializer(self):
        review_data = {
            'id': self.review.id,
            'movie': self.movie.id,
            'user': self.user.id,
            'rating': self.review.rating,
            'content': self.review.content,
            'created_at': self.review.created_at.isoformat(),
        }
        serializer = ReviewSerializer(self.review)
        self.assertEqual(serializer.data, review_data)

    def test_comment_serializer(self):
        comment_data = {
            'id': self.comment.id,
            'review': self.review.id,
            'username': self.comment.user.username,
            'user': self.comment.user.id,
            'content': self.comment.content,
            'created_at': self.comment.created_at.isoformat(),
        }
        serializer = CommentSerializer(self.comment)
        self.assertEqual(serializer.data, comment_data)

    def test_profile_serializer(self):
        profile_data = {
            'id': self.profile.id,
            'user': self.profile.user.id,
            'bio': self.profile.bio,
            'avatar': self.profile.avatar.url,
        }
        serializer = ProfileSerializer(self.profile)
        self.assertEqual(serializer.data, profile_data)

    def test_create_movie_with_genres(self):
        movie_data = {
            'title': 'New Movie',
            'release_year': 2026,
            'director': 'New Director',
            'description': 'A new test movie.',
            'genres': [self.genre1.id, self.genre2.id],
        }
        serializer = MovieSerializer(data=movie_data)
        self.assertTrue(serializer.is_valid())
        movie = serializer.save()
        self.assertEqual(movie.title, 'New Movie')
        self.assertEqual(movie.genres.count(), 2)

    def test_invalid_review_serializer(self):
        invalid_data = {'rating': 6}
        serializer = ReviewSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('rating', serializer.errors)

    def test_invalid_comment_serializer(self):
        invalid_data = {'review': self.review.id, 'user': self.user.id}
        serializer = CommentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)