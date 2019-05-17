from django.contrib.auth.models import User
from django.test import LiveServerTestCase, Client
from rest_framework.test import APIRequestFactory

from bookcase.models import Annotation, Book

requester = APIRequestFactory()


class BookViewSetTest(LiveServerTestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username='user1', email='user1@mail.com', password='1q12w23e3',
        )
        user2 = User.objects.create_user(
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
        Annotation.objects.create(
            annotation_author=user1,
            book=book1,
            text='annotation 1',
            page=1,
        )
        Annotation.objects.create(
            annotation_author=user1,
            book=book2,
            text='annotation 2',
            page=2,
        )
        Annotation.objects.create(
            annotation_author=user2,
            book=book1,
            text='annotation 3',
            page=3,
        )

        self.books = (book1, book2, book3)
        self.user1 = user1
        self.client = Client()
        self.client.login(username='user1', password='1q12w23e3')

    def test001_get(self):
        response = self.client.get('/books/')

        self.assertIsNotNone(response.data, 'No data retrieved')
        self.assertEqual(len(response.data), 3, 'Array length mismatch in unfiltered request')
        self.assertEqual(response.data[0]['title'], self.books[0].title, 'book titles don\'t match')
        self.assertEqual(response.data[0]['author']['id'], self.books[0].author.id, 'book authors don\'t match')

        response = self.client.get('/books/?has_my_annotations=true')
        self.assertEqual(len(response.data), 2, 'Array length mismatch in filtered by presence of annotation')

    def assertAdded(self, model, lookup, msg):
        try:
            obj = model.objects.get(**lookup)
        except model.DoesNotExist:
            self.fail(msg.format(**lookup))
        self.assertIsNotNone(obj, msg.format(**lookup))
        return obj

    def test002_post(self):
        response = self.client.post('/books/', data={
            'title': 'book 4',
            'number_of_pages': 4,
            'annotations': [
                {'text': 'annotation 4', 'page': 4},
                {'text': 'annotation 5', 'page': 5},
            ]
        }, content_type='application/json')

        self.assertEquals(response.status_code, 201, f'Request responded with {response.status_code}')

        response = self.client.post('/books/', data={
            'title': 'book 5',
            'number_of_pages': 5,
        }, content_type='application/json')

        self.assertEquals(response.status_code, 201, f'Request responded with {response.status_code}')

        book4 = self.assertAdded(Book, {'title': 'book 4'}, '{title} was not added')
        self.assertEquals(book4.number_of_pages, 4, 'Number of pages do not much')
        self.assertEquals(book4.author.id, self.user1.id, 'Author does not match')

        book5 = self.assertAdded(Book, {'title': 'book 5'}, '{title} was not added')
        self.assertEquals(book5.number_of_pages, 5, 'Number of pages do not much')
        self.assertEquals(book5.author.id, self.user1.id, 'Author does not match')

        annotation4 = self.assertAdded(Annotation, {'text': 'annotation 4'}, '{text} was not added')
        self.assertEquals(annotation4.annotation_author.id, self.user1.id, 'annotation 4 author does not match')
        self.assertEquals(annotation4.page, 4, 'annotation 4 page does not match')

        annotation5 = self.assertAdded(Annotation, {'text': 'annotation 5'}, '{text} was not added')
        self.assertEquals(annotation5.annotation_author.id, self.user1.id, 'annotation 5 author does not match')
        self.assertEquals(annotation5.page, 5, 'annotation 5 page does not match')
