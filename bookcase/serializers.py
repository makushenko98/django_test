from django.contrib.auth.models import User
from rest_framework.serializers import (
    ModelSerializer,
)

from bookcase.models import (
    Book,
    Annotation,
)


class AuthorSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'username')
        model = User


class BookSerializer(ModelSerializer):
    class _AnnotationSerializer(ModelSerializer):
        class Meta:
            fields = ('page', 'text')
            model = Annotation

    author = AuthorSerializer(read_only=True)
    annotations = _AnnotationSerializer(write_only=True, many=True)

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is None:
            return None

        book = self.Meta.model.objects.create(
            author=request.user,
            title=validated_data.get('title'),
            number_of_pages=validated_data.get('number_of_pages')
        )

        annotations = validated_data.get('annotations')
        if annotations:
            for entry in annotations:
                Annotation.objects.create(
                    annotation_author=request.user,
                    book=book,
                    **entry
                )

        return book

    class Meta:
        fields = ('id', 'title', 'number_of_pages', 'author', 'annotations')
        model = Book


class AnnotationSerializer(ModelSerializer):
    annotation_author = AuthorSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is None:
            return None

        return self.Meta.model.objects.create(
            annotation_author=request.user,
            text=validated_data.get('text'),
            page=validated_data.get('page'),
            book=validated_data.get('book'),
        )

    class Meta:
        fields = ('id', 'page', 'text', 'book', 'annotation_author')
        model = Annotation