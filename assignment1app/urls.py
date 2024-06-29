from django.urls import path
from .views import SongAPIView

urlpatterns = [
    path('', SongAPIView.as_view(), name='song-list-create'),
    path('<int:audioFileId>/', SongAPIView.as_view(), name='song-detail'),
    path('<str:audioFileType>/', SongAPIView.as_view(), name='song-list-by-type'),
    path('<str:audioFileType>/<int:audioFileId>/', SongAPIView.as_view(), name='song-detail-by-type'),
]
