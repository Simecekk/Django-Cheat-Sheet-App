from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseDeleteView

from hollymovies_app.models import Movie, Genre, GENRE_NAME_TO_NAME_SHORTCUT_MAPPING
from hollymovies_app.views.mixins import CurrentTimeMixing, EditMovieMixin


#####################
# Class based views #
#####################

class MovieDetailView(CurrentTimeMixing, DetailView):
    template_name = 'movie/detail.html'
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
        return redirect('movie:detail', pk=pk)


class CreateMovieView(EditMovieMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateMovieView, self).get_context_data(**kwargs)
        context.update({
            'action_url': resolve_url('movie:create')
        })
        return context


class UpdateMovieView(EditMovieMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateMovieView, self).get_context_data(**kwargs)
        context.update({
            'action_url': resolve_url('movie:update', pk=self.object.pk)
        })
        return context


class DeleteMovieView(BaseDeleteView):
    model = Movie

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('homepage')


class GenreDetailView(DetailView):
    template_name = 'genre/detail.html'
    model = Genre


########################
# Function based views #
########################

def movie_detail_view(request, pk):
    movie = Movie.objects.get(id=pk)

    if request.method == 'POST':
        movie.likes += 1
        movie.save()

    context = {
        'movie': movie,
    }
    return TemplateResponse(request, 'movie/detail.html', context=context)


def genre_detail_view(request, genre_name):
    genre_name_shortcut = GENRE_NAME_TO_NAME_SHORTCUT_MAPPING[genre_name]
    genre = Genre.objects.get(name=genre_name_shortcut)

    # Filtering only movies which have more than 10 likes
    movies = genre.movies.filter(likes__gte=10)
    context = {
        'genre': genre,
        'movies': movies,
        'page_description': {
            'long_description': 'This is long description',  # TODO Add separeted html template for explaing accesing dict values in template
            'short_description': 'This is short description'
        },
        'creators': ['Jan', 'Pepa']
    }
    return TemplateResponse(request, 'genre/detail.html', context=context)

