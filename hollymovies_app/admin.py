from django.contrib import admin

from hollymovies_app.models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Movie, MovieAdmin)
