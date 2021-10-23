from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseDeleteView, FormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from hollymovies_app.forms import ContactForm, MovieForm, RegistrationForm
from hollymovies_app.models import Movie, Genre, GENRE_NAME_TO_NAME_SHORTCUT_MAPPING


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('homepage')


class LoginView(FormMixin, TemplateView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Log in successfully')
            return redirect('homepage')

        messages.error(request, 'Wrong credentials')
        return redirect('login')


class RegistrationView(FormMixin, TemplateView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm

    def post(self, request,  *args, **kwargs):
        registration_data = request.POST
        form = self.form_class(registration_data)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account {form.cleaned_data.get("username")} successfully created')
            return redirect('login')
        else:
            messages.error(request, f'Something wrongs')
            return TemplateResponse(request, 'accounts/registration.html', context={'form': form})


def homepage_view(request):
    """ Function base view """
    movies_db = Movie.objects.all().order_by('-likes', 'name')

    context = {
        'movies': movies_db,
        'horror_genre': Genre.HORROR,
    }
    return TemplateResponse(request, 'homepage.html', context=context)


class CurrentTimeMixing:
    """
        https://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-are-they-useful
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.now().isoformat()
        })
        return context


class HomepageView(CurrentTimeMixing, TemplateView):
    """
     CBV - Class-based views

     https://stackoverflow.com/questions/14788181/class-based-views-vs-function-based-views
    """
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


def movie_detail_view(request, pk):
    movie = Movie.objects.get(id=pk)

    if request.method == 'POST':
        movie.likes += 1
        movie.save()

    context = {
        'movie': movie,
    }
    return TemplateResponse(request, 'detail/movie_detail.html', context=context)


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


def genre_detail_view(request, genre_name):
    genre_name_shortcut = GENRE_NAME_TO_NAME_SHORTCUT_MAPPING[genre_name]
    genre = Genre.objects.get(name=genre_name_shortcut)

    # Filtering only movies which have more than 10 likes
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


class ContactView(PermissionRequiredMixin, View):
    permission_required = 'dummyApp.can_create_contact'

    def get(self, request, *args, **kwargs):
        context = {
            'contact_form': ContactForm(),
        }
        return TemplateResponse(request, 'contact.html', context=context)

    def post(self, request, *args, **kwargs):
        # Form is bounded when we bound data to it
        bounded_contact_form = ContactForm(request.POST)

        if not bounded_contact_form.is_valid():
            context = {'contact_form': bounded_contact_form}
            return TemplateResponse(request, 'contact.html', context=context)

        # Now we can do whatever we want with the data
        # NOTE: We have to call is_valid() before accessing cleaned_data on the form
        name = bounded_contact_form.cleaned_data['name']
        email = bounded_contact_form.cleaned_data['email']
        subject = bounded_contact_form.cleaned_data['subject']
        description = bounded_contact_form.cleaned_data['description']

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
            'action_url': resolve_url('create_movie')
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

