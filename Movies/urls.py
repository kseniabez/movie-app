from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('account/', views.user_account, name='user_account'),
    path('user/<int:user_id>/reviews/', views.user_reviews, name='user_reviews'),
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<int:user_id>/', views.user_account, name='user_account'),
    path('movies/', views.movies_view, name='movies'),
    path('movies/<int:movie_id>/', views.movie_detail_view, name='movie_detail'),
    path('user/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('write-review/<int:movie_id>/', views.write_review, name='write-review'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset_form'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate')
]