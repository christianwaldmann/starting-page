from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Bookmarks
from .serializers import BookmarksSerializer


class ListBookmarksView(generics.ListCreateAPIView):
    """
    GET bookmarks/
    Post bookmarks/
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = BookmarksSerializer

    def get_queryset(self):
        return self.request.user.bookmarks.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookmarksDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET bookmarks/:id/
    PUT bookmarks/:id/
    DELETE bookmarks/:id/
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = BookmarksSerializer

    def get_queryset(self):
        return self.request.user.bookmarks.all()
