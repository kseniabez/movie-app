from rest_framework.routers import DefaultRouter
from .viewsets import GenreViewSet, MovieViewSet, ReviewViewSet, CommentViewSet, ProfileViewSet

router = DefaultRouter()

router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'profiles', ProfileViewSet)
urlpatterns = router.urls