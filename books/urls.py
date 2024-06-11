from django.urls import path, include
from rest_framework import routers

from books.viewsets import BookViewSet, AuthorViewSet, GenreViewSet, PublisherViewSet

app_name = 'books'

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'publishers', PublisherViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
