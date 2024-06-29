from rest_framework import generics, status
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer

class SongAPIView(generics.GenericAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.all()

    def get(self, request, audioFileType=None, audioFileId=None):
        # Retrieve a specific song by ID if provided
        if audioFileId:
            try:
                song = self.get_queryset().get(pk=audioFileId)
                serializer = self.serializer_class(song)
                return Response(serializer.data)
            except Song.DoesNotExist:
                return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all songs filtered by audio file type if provided
        if audioFileType:
            songs = self.get_queryset().filter(audio_file__icontains=audioFileType)
            serializer = self.serializer_class(songs, many=True)
            return Response(serializer.data)

        # Retrieve all songs without filtering by audio file type
        songs = self.get_queryset()
        serializer = self.serializer_class(songs, many=True)
        return Response(serializer.data)

    def post(self, request, audioFileType=None):
        if audioFileType and audioFileType != 'song':
            return Response({"error": "Invalid audio file type"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, audioFileType=None, audioFileId=None):
        if audioFileType and audioFileType != 'song':
            return Response({"error": "Invalid audio file type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            song = self.get_queryset().get(pk=audioFileId)
        except Song.DoesNotExist:
            return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, audioFileType=None, audioFileId=None):
        if audioFileType and audioFileType != 'song':
            return Response({"error": "Invalid audio file type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            song = self.get_queryset().get(pk=audioFileId)
        except Song.DoesNotExist:
            return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

        song.delete()
        return Response({"message": "Song deleted"}, status=status.HTTP_200_OK)
