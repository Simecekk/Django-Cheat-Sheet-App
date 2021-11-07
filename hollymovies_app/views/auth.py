from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from hollymovies_app.forms.auth import RegistrationForm


#####################
# Class based views #
#####################


class LogoutView(View):
    """
    NOTE: Django has built it LogoutView (from django.contrib.auth.views import LogoutView)
    but this django LogoutView expect us to have logout template.

    In our case we will have LogoutView in the base template. So we implement it ourselves.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('homepage')


class LoginView(FormMixin, TemplateView):
    """
    NOTE: Django has built it LoginView (from django.contrib.auth.views import LoginView).

    Reason why I'm not using it is that I wanted to explain how is it done under the hood
    """
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
        return redirect('auth:login')


class RegistrationView(FormMixin, TemplateView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm

    def post(self, request,  *args, **kwargs):
        registration_data = request.POST
        form = self.form_class(registration_data)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account {form.cleaned_data.get("username")} successfully created')
            return redirect('auth:login')
        else:
            messages.error(request, f'Something wrongs')
            return TemplateResponse(request, 'accounts/registration.html', context={'form': form})


########################
# Function based views #
########################


def logout_view(request):
    logout(request)


def login_view(request):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm(),
        }
        return TemplateResponse(request, 'accounts/login.html', context=context)

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Log in successfully')
            return redirect('homepage')

        messages.error(request, 'Wrong credentials')
        return redirect('auth:login')


def registration_view(request):
    if request.method == 'GET':
        context = {
            'form': RegistrationForm(),
        }
        return TemplateResponse(request, 'accounts/registration.html', context=context)

    elif request.method == 'POST':
        registration_data = request.POST
        form = RegistrationForm(registration_data)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account {form.cleaned_data.get("username")} successfully created')
            return redirect('auth:login')
        else:
            messages.error(request, f'Something wrongs')
            return TemplateResponse(request, 'accounts/registration.html', context={'form': form})
