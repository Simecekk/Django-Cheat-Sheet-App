from django.shortcuts import resolve_url
from django.utils import timezone

from hollymovies_app.forms.movie import MovieForm
from hollymovies_app.models import Movie


# ? NOTE: https://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-are-they-useful

class CurrentTimeMixing:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.now().isoformat()
        })
        return context


class EditMovieMixin:
    template_name = 'create.html'
    form_class = MovieForm
    model = Movie

    def get_success_url(self):
        return resolve_url('movie:detail', pk=self.object.id)
