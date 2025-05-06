from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review, Comment, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, CommentForm, ProfileForm, ReviewForm
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str


def home(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'reviews': reviews})

def about(request):
    return render(request, 'about.html')

def user_account(request, user_id):
    user_acc = get_object_or_404(User, id=user_id)
    user_reviews = Review.objects.filter(user=user_acc).order_by('-created_at')
    is_own_account = request.user == user_acc

    try:
        profile = user_acc.profile
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'user-account.html', {
        'user_acc': user_acc,
        'user_reviews': user_reviews,
        'is_own_account': is_own_account,
        'profile': profile,
    })

def user_reviews(request, user_id):
    reviews = Review.objects.filter(user__id=user_id)
    return render(request, 'movies/review-list.html', {'reviews': reviews})


def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    comments = review.comments.all().order_by('-created_at')

    if request.method == 'POST' and 'delete_review' in request.POST and request.user == review.user:
        review.comments.all().delete()
        # Delete the review
        review.delete()
        messages.success(request, "Review and associated comments deleted successfully!")
        return redirect('home')

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
            return redirect('review_detail', review_id=review.id)
    else:
        form = CommentForm()

    return render(request, 'movies/review.html', {
        'review': review,
        'comments': comments,
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Generate activation email
            current_site = get_current_site(request)
            subject = "Activate Your Account"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"{request.scheme}://{current_site.domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"

            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            send_mail(subject, message, 'webmaster@example.com', [user.email], fail_silently=False)

            messages.success(request, "Account created! Please check your email to activate your account.")
            return render(request, 'registration/activation.html', {'activated': False})
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activation.html', {'activated': True})
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return render(request, 'registration/activation.html', {'activated': False})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def movies_view(request):
    movies = Movie.objects.all().order_by('title')
    paginator = Paginator(movies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movies/movies.html', {'page_obj': page_obj})

def movie_detail_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.order_by('-created_at')[:10]
    return render(request, 'movies/movie-detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def edit_profile(request, user_id):
    user_acc = get_object_or_404(User, id=user_id)

    if request.user != user_acc:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('profile')

    try:
        profile = user_acc.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_account', user_id=user_acc.id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit-profile.html', {'form': form, 'profile': profile})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('review_detail', review_id=review.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'movies/review-form.html', {
        'page_title': 'Edit Review',
        'heading': f'Edit Review',
        'movie': review.movie,
        'form': form,
        'button_text': 'Save Changes',
        'cancel_url': reverse('review_detail', args=[review.id]),
    })


@login_required
def write_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()

    return render(request, 'movies/review-form.html', {
        'page_title': 'Write a Review',
        'heading': 'Write a New Review',
        'movie': movie,
        'form': form,
        'button_text': 'Save Review',
        'cancel_url': None,
    })