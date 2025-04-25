from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import File
from .serializers import FileUploadSerializer
from django.http import Http404 , FileResponse
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.shortcuts import render

# File Upload View (Only for Ops Users)
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle file upload. Only allowed for Ops users.
        """
        if not request.user.is_ops_user:
            return Response({"error": "You are not authorized to upload files."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            file = serializer.save()
            return Response({"msg": "File uploaded successfully", "file_id": file.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# File List View (For Client Users)
class FileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all files uploaded by Ops users (For Client Users).
        """
        if not request.user.is_client_user:
            return Response({"error": "You are not authorized to view files."}, status=status.HTTP_403_FORBIDDEN)

        
        files = File.objects.filter(uploaded_by__is_ops_user=True)  
        file_data = [{"id": file.id, "file_name": file.file_name} for file in files]
        return Response(file_data)


# File Download View (For Client Users)

class FileDownloadView(APIView):
    def get(self, request, file_id):
        try:
            # Fetch the file from the database based on file_id
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            raise Http404("File not found.")
        
        # Construct the absolute file path
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

        # Check if the file exists on the disk
        if not os.path.exists(file_path):
            raise Http404("File does not exist on disk.")
        
        # Generate the download link
        download_url = request.build_absolute_uri(f'{settings.MEDIA_URL}{file.file.name}')

        # Return the download URL in a JSON response
        return Response({"download_url": download_url}, status=status.HTTP_200_OK)