from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter


from bookcase.views import (
    BookViewSet,
    AnnotationViewSet,
)

router = SimpleRouter()
router.register('books', BookViewSet)
router.register('annotations', AnnotationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
