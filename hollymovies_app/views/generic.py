from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView

from hollymovies_app.forms.generic import ContactForm
from hollymovies_app.models import Movie, Genre
from hollymovies_app.views.mixins import CurrentTimeMixing


#######################
# Classed based views #
#######################

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


########################
# Function based views #
########################

def homepage_view(request):
    """ Function base view """
    movies_db = Movie.objects.all().order_by('-likes', 'name')

    context = {
        'movies': movies_db,
        'horror_genre': Genre.HORROR,
    }
    return TemplateResponse(request, 'homepage.html', context=context)


@permission_required('dummyApp.can_create_contact')
def contact_view(request):
    if request.method == 'GET':
        context = {
         'contact_form': ContactForm(),
        }
        return TemplateResponse(request, 'contact.html', context=context)
    elif request.method == 'POST':
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

