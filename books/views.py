from rest_framework import generics

from library.serializers import (
    BookDetailSerializer
)

from library.models import Book


class BookList(generics.ListAPIView):
    model = Book
    serializer_class = BookDetailSerializer
    queryset = Book.objects.all().order_by('-created')

    def get_queryset(self):
        """
        This view should return a list of books.
        """
        return Book.objects.all().select_related(
            'book_type',
            'publisher',).prefetch_related(
            'authors',
            'keywords')
