from django.http import HttpResponse
from django.template.response import TemplateResponse

from hollymovies_app.models import Movie, Genre, GENRE_NAME_TO_NAME_SHORTCUT_MAPPING


def homepage(request):
    movies_db = Movie.objects.all()  # SELECT * FROM hollymoviesapp_movie;
    context = {
        'movies': movies_db,
        'horror_genre': Genre.HORROR,
    }
    return TemplateResponse(request, 'homepage.html', context=context)


def movie_detail(request, pk):
    movie = Movie.objects.get(id=pk)
    context = {
        'movie': movie,
    }
    return TemplateResponse(request, 'movie_detail.html', context=context)


def genre_detail(request, genre_name):
    genre_name_shortcut = GENRE_NAME_TO_NAME_SHORTCUT_MAPPING[genre_name]
    genre = Genre.objects.get(name=genre_name_shortcut)
    context = {
        'genre': genre
    }
    return TemplateResponse(request, 'genre_detail.html', context=context)


def homepage_david(request):
    return HttpResponse('<h1>Hollymovies Homepage David</h1>')
