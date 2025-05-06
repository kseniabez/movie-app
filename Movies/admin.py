from django.contrib import admin
from Movies.models import Movie, Review, Comment, Genre, Profile

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Profile)