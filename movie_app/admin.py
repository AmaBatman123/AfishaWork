from django.contrib import admin
from movie_app.models import Director, Movie, Review, ConfirmationCode

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(ConfirmationCode)

