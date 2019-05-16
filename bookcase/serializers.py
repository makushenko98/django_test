from rest_framework.serializers import (
    ModelSerializer,
)

from bookcase.models import (
    Book,
    Annotation,
)


class BookSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'number_of_pages', 'author')
        model = Book



class AnnotationSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'page', 'text', 'book', 'annotation_author')
        model = Annotation
