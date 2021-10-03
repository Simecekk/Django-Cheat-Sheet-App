from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True


class Genre(BaseModel):
    HORROR = 'HR'
    COMEDY = 'CM'
    GENRE_NAME_CHOICES = [
        (HORROR, 'Horror'),
        (COMEDY, 'Comedy'),
    ]
    name = models.CharField(choices=GENRE_NAME_CHOICES, max_length=2, unique=True)

    def is_genre_horror(self) -> bool:
        return self.name == self.HORROR

    def is_genre_comedy(self) -> bool:
        return self.name == self.COMEDY

    def __str__(self):
        return f'{self.get_name_display()} : {self.id}'

    def get_url_slug(self):
        return self.get_name_display().lower()


GENRE_NAME_TO_NAME_SHORTCUT_MAPPING = {
    'horror': Genre.HORROR,
    'comedy': Genre.COMEDY,
}


class Movie(BaseModel):
    name = models.CharField(max_length=512)
    likes = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return f'{self.name} : {self.id}'


class Person(BaseModel):
    name = models.CharField(max_length=512)
    age = models.IntegerField()
    description = models.TextField()

    class Meta:
        abstract = True


class Actor(Person):
    name = models.CharField(max_length=512)
    movies = models.ManyToManyField(Movie, related_name='actors')
