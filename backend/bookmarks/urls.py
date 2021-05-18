from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListBookmarksView, BookmarksDetailView

urlpatterns = [
    path('api/bookmarks/', ListBookmarksView.as_view(), name="bookmarks-all"),
    path('api/bookmarks/<int:pk>/', BookmarksDetailView.as_view(),
         name="bookmarks-detail")
]

urlpatterns = format_suffix_patterns(urlpatterns)
