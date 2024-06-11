from django.db import models

from .author import Author
from .genre import Genre
from .publisher import Publisher


class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    pages = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title
