from rest_framework.serializers import (
    ModelSerializer,
)


class BookSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'number_of_pages', 'author')


class AnnotationSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'page', 'text', 'book', 'annotation_author')
