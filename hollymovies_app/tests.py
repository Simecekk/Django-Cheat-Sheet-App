from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve

from hollymovies_app.forms.movie import MovieForm
from hollymovies_app.models import Movie, Genre
from hollymovies_app.views.generic import HomepageView
from hollymovies_app.views.movie import genre_detail_view


class TestUrls(SimpleTestCase):
    """
         NOTED: SimpleTestCase is used when we don't need to interact with db.
         docs: https://docs.djangoproject.com/en/3.2/topics/testing/tools/#simpletestcase
    """

    def test_homepage_url_is_resolved(self):
        """ Class based views resolve test """
        url = reverse('homepage')
        self.assertEqual(resolve(url).func.view_class, HomepageView)

    # def test_genre_detail_url_is_resolved(self):
    #     """ function based views resolve test """
    #     url = reverse('genre:detail', args=['testing_genre'])
    #     self.assertEqual(resolve(url).func, genre_detail_view)


class TestViews(TestCase):

    def setUp(self):
        """ This method is run before every test_ method defined in the TestCase """
        self.client = Client()
        self.movie = Movie.objects.create(name='Testing Movie')

    @classmethod
    def setUpClass(cls):
        """ This is run once when the whole TestCase starts """
        super(TestViews, cls).setUpClass()

    def test_homepage_GET(self):
        url = reverse('homepage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'homepage.html')

    def test_movie_detail_GET(self):
        # Test Non-Existing movie detail
        url = reverse('movie:detail', args=[999999999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # Test Existing movie detail
        url = reverse('movie:detail', args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_movie_detail_POST(self):
        url = reverse('movie:detail', args=[self.movie.id])
        response = self.client.post(url)
        self.movie.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.movie.likes, 1)


class TestModels(TestCase):

    def setUp(self):
        self.horror = Genre.objects.create(name=Genre.HORROR)
        self.comedy = Genre.objects.create(name=Genre.COMEDY)

        self.movie_1 = Movie.objects.create(
            name='Testing Movie 1',
            likes=10
        )
        self.movie_2 = Movie.objects.create(
            name='Testing Movie 2',
            likes=20
        )
        self.movie_3 = Movie.objects.create(
            name='Testing Movie 3',
            likes=30,
        )
        self.movie_4 = Movie.objects.create(
            name='Testing Movie 4',
            likes=6,
        )

    def test_genre_is_horror(self):
        self.assertTrue(self.horror.is_genre_horror())

    def test_genre_is_comedy(self):
        self.assertTrue(self.comedy.is_genre_comedy())

    def test_get_movies_with_at_least_10_likes(self):
        movies_with_at_least_10_likes = Movie.get_movies_with_at_least_10_likes()
        self.assertEqual(movies_with_at_least_10_likes.count(), 3)
        for movie in movies_with_at_least_10_likes:
            self.assertTrue(movie.likes >= 10)

    def test_movie_has_at_least_than_10_likes(self):
        self.assertFalse(self.movie_4.has_at_least_than_10_likes)
        self.assertTrue(self.movie_2.has_at_least_than_10_likes)


class TestForms(TestCase):

    def test_movie_form_is_valid(self):
        genre = Genre.objects.create(name=Genre.HORROR)
        form = MovieForm(data={
            'name': 'Rambo 1',
            'description': 'Just another Rambo movie',
            'genres': [genre.id],
        })
        self.assertTrue(form.is_valid())

    def test_movie_form_is_invalid(self):
        form = MovieForm(data={})
        self.assertFalse(form.is_valid())
