from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bookcase.models import (
    Book,
    Annotation
)
from bookcase.serializers import (
    BookSerializer,
    AnnotationSerializer,
)
from bookcase.permissions import (
    IsAuthorOrReadOnly,
)


class BookViewSet(ModelViewSet):
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AnnotationViewSet(ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
