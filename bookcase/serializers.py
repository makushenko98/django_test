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
    author = AuthorSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is None:
            return None
        return self.Meta.model.objects.create(
            author=request.user,
            title=validated_data.get('title'),
            number_of_pages=validated_data.get('number_of_pages')
        )

    class Meta:
        fields = ('id', 'title', 'number_of_pages', 'author')
        model = Book


class AnnotationSerializer(ModelSerializer):
    annotation_author = AuthorSerializer()

    class Meta:
        fields = ('id', 'page', 'text', 'book', 'annotation_author')
        model = Annotation
