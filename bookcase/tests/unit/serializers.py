from django.contrib.auth.models import User
from django.test import TestCase
import io
from rest_framework.parsers import JSONParser

from bookcase.serializers import BookSerializer
from bookcase.models import Annotation, Book
from rest_framework.test import APIRequestFactory, force_authenticate

valid_json_with_1_annotation = b'{"title":"book","number_of_pages":3,\
 "annotations":[{"text":"annotation1","page":1}]}'

invalid_json_1 = b'{"title":"b6lJzLxj2ELX3fqkmFAAIEDztQkQWUz4oqWKqWisKp6jvf7NIo1" }'

requester = APIRequestFactory()


def parse_json(json_bytes):
    return JSONParser().parse(
        io.BytesIO(json_bytes)
    )


class MockRequest:
    def __init__(self, user, method='GET'):
        self.user = user
        self.method = method


class BookSerializerTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(
            username='user1', email='user1@mail.com', password='1q12w23e3',
        )

        book1 = Book.objects.create(
            title='book 1',
            number_of_pages=10,
            author=user1,
        )

        self.user1 = user1

    def assertSerializerValid(self, json, should_be_valid):
        serializer = BookSerializer(data=parse_json(json))
        serializer.context['request'] = MockRequest(self.user1, 'PATCH')
        msg = 'Serializer results should be considered {0}'.format(
            'valid' if should_be_valid else 'invalid'
        )
        is_valid = serializer.is_valid()
        self.assertEqual(is_valid, should_be_valid, msg)

    def test001_validation(self):
        book_serializer = BookSerializer(data=parse_json(
            valid_json_with_1_annotation
        ))
        book_serializer.context['request'] = MockRequest(self.user1)

        self.assertTrue(book_serializer.is_valid(), 'Serializer results should be considered valid')

        def wrong(something):
            return f'{something} don\' match input'

        self.assertEqual(book_serializer.validated_data.get('title'), 'book', wrong('Title'))
        self.assertEqual(book_serializer.validated_data.get('number_of_pages'), 3, wrong('Number of pages'))
        annotations = book_serializer.validated_data.get('annotations')
        self.assertIsNotNone(annotations, 'No annotations')
        self.assertIsNotNone(annotations[0], 'No annotations')
        self.assertEquals(annotations[0].get('text'), 'annotation1', wrong('Annotation text'))
        self.assertEquals(annotations[0].get('page'), 1, wrong('Annotation page'))
        self.assertSerializerValid(invalid_json_1, False)

    def test002_creation(self):
        book_serializer = BookSerializer(data=parse_json(
            valid_json_with_1_annotation
        ))

        def book_wrong(something):
            return f'Created book has wrong {something}'

        book_serializer.context['request'] = MockRequest(self.user1)

        book_serializer.is_valid()
        book_serializer.save()

        book = Book.objects.get(title='book')
        self.assertIsNotNone(book, f'Book wasn\'t created or {book_wrong("title")}')
        self.assertEquals(book.number_of_pages, 3, book_wrong('number of pages'))
        self.assertEquals(book.author, self.user1, book_wrong('author'))

        def ann_wrong(something):
            return f'Created annotation has wrong {something}'

        annotation = Annotation.objects.get(text="annotation1")
        self.assertIsNotNone(annotation, f'Annotation wasn\'t created or {ann_wrong("text")}')
        self.assertEquals(annotation.page, 1, ann_wrong('page'))
        self.assertEquals(annotation.annotation_author, self.user1, ann_wrong('author'))
