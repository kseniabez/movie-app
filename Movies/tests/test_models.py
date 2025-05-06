from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User

from Movies.models import Genre, Movie, Review, Comment, Profile

class MovieModelTest(TestCase):

    def setUp(self):
        # Create a Genre instance
        self.genre = Genre.objects.create(name='Action')
        # Create a Movie instance
        self.poster_image = SimpleUploadedFile(name='test_poster.jpg', content=b'', content_type='image/jpeg')
        self.movie = Movie.objects.create(
            title='Test Movie',
            release_year=2025,
            director='Test Director',
            description='Test Description',
            poster_image=self.poster_image
        )
        # Add genre to movie
        self.movie.genres.add(self.genre)

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.release_year, 2025)
        self.assertEqual(self.movie.director, 'Test Director')
        self.assertEqual(self.movie.description, 'Test Description')
        self.assertTrue(self.movie.poster_image.name.startswith('posters/'))

    def test_movie_genre(self):
        self.assertIn(self.genre, self.movie.genres.all())

    def test_movie_string_representation(self):
        self.assertEqual(str(self.movie), 'Test Movie')

class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.movie = Movie.objects.create(
            title='Test Movie',
            release_year=2025,
            director='Test Director',
            description='Test Description',
            poster_image='posters/test_poster.jpg'
        )
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=5,
            content='Great movie!'
        )

    def test_review_creation(self):
        self.assertEqual(self.review.movie.title, 'Test Movie')
        self.assertEqual(self.review.user.username, 'testuser')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.content, 'Great movie!')

    def test_review_string_representation(self):
        self.assertEqual(str(self.review), f"Review for {self.movie.title} by {self.user.username}")

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.movie = Movie.objects.create(
            title='Test Movie',
            release_year=2025,
            director='Test Director',
            description='Test Description',
            poster_image='posters/test_poster.jpg'
        )
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=5,
            content='Great movie!'
        )
        self.comment = Comment.objects.create(
            review=self.review,
            user=self.user,
            content='Great review!'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.review.content, 'Great movie!')
        self.assertEqual(self.comment.user.username, 'testuser')
        self.assertEqual(self.comment.content, 'Great review!')

    def test_comment_string_representation(self):
        self.assertEqual(str(self.comment), f"Comment by {self.user.username} on {self.review.movie.title}")
