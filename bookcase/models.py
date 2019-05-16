from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=50)
    number_of_pages = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Annotation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    page = models.IntegerField()
    annotation_author = models.ForeignKey(User, on_delete=models.CASCADE)
