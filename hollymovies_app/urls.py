from django.urls import path


from hollymovies_app.views import genre_detail, HomepageView, MovieDetailView, ResetMovieLikesView, ContactView, \
    CreateMovieView

urlpatterns = [
    path('homepage/', HomepageView.as_view(), name='homepage'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('genre/<str:genre_name>/', genre_detail, name='genre_detail'),
    path('movie/reset-likes/<int:pk>', ResetMovieLikesView.as_view(), name='movie-reset-likes'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('create_movie/', CreateMovieView.as_view(), name='create_movie')
]
