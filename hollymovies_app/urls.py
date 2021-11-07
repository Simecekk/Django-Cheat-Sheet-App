from django.urls import path, include

from hollymovies_app.views.auth import LoginView, LogoutView, RegistrationView
from hollymovies_app.views.generic import HomepageView, ContactView
from hollymovies_app.views.movie import MovieDetailView, UpdateMovieView, DeleteMovieView, genre_detail_view, \
    ResetMovieLikesView, CreateMovieView

movie_urlpatterns = ([
    path('<int:pk>/', MovieDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', UpdateMovieView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteMovieView.as_view(), name='delete'),
    path('<int:pk>/reset-likes/', ResetMovieLikesView.as_view(), name='reset-likes'),
    path('create_movie/', CreateMovieView.as_view(), name='create'),
], 'movie')

genre_urlpatterns = ([
    path('genre/<str:genre_name>/', genre_detail_view, name='detail'),
], 'genre')

auth_urlpatterns = ([
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
], 'auth')

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('movie/', include(movie_urlpatterns)),
    path('genre/', include(genre_urlpatterns)),
    path('auth/', include(auth_urlpatterns)),
]
