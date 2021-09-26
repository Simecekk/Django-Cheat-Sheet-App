from django.urls import path

from hollymovies_app.views import homepage, movie_detail

urlpatterns = [
    path('homepage/', homepage, name='homepage'),
    path('movie/<int:pk>/', movie_detail, name='movie_detail')
]
