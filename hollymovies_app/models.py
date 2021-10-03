from django.db import models


class Genre(models.Model):
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


class Movie(models.Model):
    # TODO Add Created Modified  --> Probrat order_by()
    name = models.CharField(max_length=512)
    likes = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return f'{self.name} : {self.id}'
