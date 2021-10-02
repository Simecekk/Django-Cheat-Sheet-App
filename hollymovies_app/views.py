from django.http import HttpResponse
from django.template.response import TemplateResponse

from hollymovies_app.models import Movie, Genre


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


def homepage_david(request):
    return HttpResponse('<h1>Hollymovies Homepage David</h1>')
