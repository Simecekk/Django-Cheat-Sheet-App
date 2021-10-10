from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin

from hollymovies_app.models import Movie, Genre, GENRE_NAME_TO_NAME_SHORTCUT_MAPPING


def homepage(request):
    movies_db = Movie.objects.all().order_by('-likes', 'name')

    if request.method != 'GET':
        raise Exception

    context = {
        'movies': movies_db,
        'horror_genre': Genre.HORROR,
    }
    return TemplateResponse(request, 'homepage.html', context=context)


class CurrentTimeMixing:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.now().isoformat()
        })
        return context


class HomepageView(CurrentTimeMixing, TemplateView):
    template_name = 'homepage.html'
    extra_context = {
        'movies': Movie.objects.all().order_by('-likes', 'name'),
        'horror_genre': Genre.HORROR,
    }

# def movie_detail(request, pk):
#     movie = Movie.objects.get(id=pk)
#
#     if request.method == 'POST':
#         movie.likes += 1
#         movie.save()
#
#     context = {
#         'movie': movie,
#     }
#     return TemplateResponse(request, 'detail/movie_detail.html', context=context)


class MovieDetailView(CurrentTimeMixing, DetailView):
    template_name = 'detail/movie_detail.html'
    model = Movie

    def post(self, request, pk, *args, **kwargs):
        movie = self.get_object()
        movie.likes += 1
        movie.save()
        return self.get(request, pk, *args, **kwargs)


class ResetMovieLikesView(SingleObjectMixin, View):
    model = Movie

    def post(self, request, pk, *args, **kwargs):
        movie = self.get_object()
        movie.likes = 0
        movie.save()
        return redirect('movie_detail', pk=pk)


def genre_detail(request, genre_name):
    genre_name_shortcut = GENRE_NAME_TO_NAME_SHORTCUT_MAPPING[genre_name]
    genre = Genre.objects.get(name=genre_name_shortcut)
    movies = genre.movies.filter(likes__gte=10)
    context = {
        'genre': genre,
        'movies': movies,
        'page_description': {
            'long_description': 'This is long description',
            'short_description': 'This is short description'
        },
        'creators': ['Jan', 'Pepa']
    }
    return TemplateResponse(request, 'detail/genre_detail.html', context=context)


def homepage_david(request):
    return HttpResponse('<h1>Hollymovies Homepage David</h1>')
