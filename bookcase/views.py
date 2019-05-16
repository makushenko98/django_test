from rest_framework.viewsets import ModelViewSet

from bookcase.models import (
    Book,
    Annotation
)

from bookcase.serializers import (
    BookSerializer,
    AnnotationSerializer,
)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AnnotationViewSet(ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
