from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve

from hollymovies_app.models import Movie
from hollymovies_app.views import HomepageView, genre_detail_view


class TestUrls(SimpleTestCase):
    """
         NOTED: SimpleTestCase is used when we don't need to interact with db.
         docs: https://docs.djangoproject.com/en/3.2/topics/testing/tools/#simpletestcase
    """

    def test_homepage_url_is_resolved(self):
        """ Class based views resolve test """
        url = reverse('homepage')
        self.assertEqual(resolve(url).func.view_class, HomepageView)

    def test_genre_detail_url_is_resolved(self):
        """ function based views resolve test """
        url = reverse('genre_detail', args=['testing_genre'])
        self.assertEqual(resolve(url).func, genre_detail_view)


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
