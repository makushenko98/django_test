from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from bookcase.views import BookViewSet
from bookcase.models import Annotation, Book


"""

requester = APIRequestFactory()
def BookViewSetTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(
            username='user1', email='user1@mail.com', password='1q12w23e3',
        )
        user2 = User.objects.create(
            username='user2', email='user2@mail.com', password='1q12w23e3',
        )

        book1 = Book.objects.create(
            title='book 1',
            number_of_pages=10,
            author=user1,
        )

        book2 = Book.objects.create(
            title='book 2',
            number_of_pages=20,
            author=user2,
        )

        book3 = Book.objects.create(
            title='book 3',
            number_of_pages=30,
            author=user1,
        )

        annotation1 = Annotation.objects.create(
            annotation_author=user1,
            book=book1,
            text='annotation 1',
            page=1,
        )

        annotation2 = Annotation.objects.create(
            annotation_author=user2,
            book=book2,
            text='annotation 2',
            page=2,
        )

        annotation3 = Annotation.objects.create(
            annotation_author=user2,
            book=book1,
            text='annotation 3',
            page=3,
        )
"""