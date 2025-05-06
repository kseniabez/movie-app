from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Movies.models import Review, Movie

class HomeViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.movie = Movie.objects.create(
            title='Test Movie', release_year=2025, director='Test Director', description='Test Description', poster_image='posters/4.jpg'
        )
        self.review = Review.objects.create(
            movie=self.movie, user=self.user, rating=5, content='Great movie!'
        )
        self.url = reverse('home')

    def test_home_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Great movie!')

class AboutViewTest(TestCase):

    def test_about_view(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')

class UserAccountViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = self.user.profile

    def test_user_account_view(self):
        url = reverse('user_account', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

class UserReviewsViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.movie = Movie.objects.create(
            title='Test Movie', release_year=2025, director='Test Director', description='Test Description', poster_image='posters/4.jpg'
        )
        self.review = Review.objects.create(
            movie=self.movie, user=self.user, rating=5, content='Great movie!'
        )

    def test_user_reviews_view(self):
        url = reverse('user_reviews', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.content)

class ReviewDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.movie = Movie.objects.create(
            title='Test Movie', release_year=2025, director='Test Director', description='Test Description', poster_image='posters/4.jpg'
        )
        self.review = Review.objects.create(
            movie=self.movie, user=self.user, rating=5, content='Great movie!'
        )
        self.url = reverse('review_detail', args=[self.review.id])

    def test_review_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.content)


class MoviesViewTest(TestCase):

    def setUp(self):
        for i in range(20):
            Movie.objects.create(
                title=f'Movie {i}', release_year=2025, director='Test Director', description='Test Description', poster_image='posters/4.jpg'
            )
        self.url = reverse('movies')

    def test_movies_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie')

class MovieDetailViewTest(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie', release_year=2025, director='Test Director', description='Test Description', poster_image='posters/4.jpg'
        )
        self.url = reverse('movie_detail', args=[self.movie.id])

    def test_movie_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)