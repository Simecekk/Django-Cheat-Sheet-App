from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=512)
    likes = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f'{self.name} : {self.id}'
