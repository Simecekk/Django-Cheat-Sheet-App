from django.http import HttpResponse
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseDeleteView

from hollymovies_app.forms import ContactForm, MovieForm
from hollymovies_app.models import Movie, Genre, GENRE_NAME_TO_NAME_SHORTCUT_MAPPING


def homepage(request):
    movies_db = Movie.objects.all().order_by('-likes', 'name')

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
        'horror_genre': Genre.HORROR,
    }

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context.update({
            'movies': Movie.objects.all().order_by('-likes', 'name'),
        })
        return context


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


class ContactView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'contact_form': ContactForm(),
        }
        return TemplateResponse(request, 'contact.html', context=context)

    def post(self, request, *args, **kwargs):
        bounded_contact_form = ContactForm(request.POST)

        if not bounded_contact_form.is_valid():
            context = {'contact_form': bounded_contact_form}
            return TemplateResponse(request, 'contact.html', context=context)

        name = bounded_contact_form.cleaned_data['name']
        email = bounded_contact_form.cleaned_data['email']
        subject = bounded_contact_form.cleaned_data['subject']
        description = bounded_contact_form.cleaned_data['description']

        print(name)
        print(email)
        print(subject)
        print(description)

        return redirect('contact')


class EditMovieMixin:
    template_name = 'create_movie.html'
    form_class = MovieForm
    model = Movie

    def get_success_url(self):
        return resolve_url('movie_detail', pk=self.object.id)


class CreateMovieView(EditMovieMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateMovieView, self).get_context_data(**kwargs)
        context.update({
            'action_url': reverse('create_movie')
        })
        return context


class UpdateMovieView(EditMovieMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateMovieView, self).get_context_data(**kwargs)
        context.update({
            'action_url': resolve_url('update_movie', pk=self.object.pk)
        })
        return context


class DeleteMovieView(BaseDeleteView):
    model = Movie

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('homepage')

