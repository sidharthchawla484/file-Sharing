from django.urls import path
from .views import FileUploadView, FileListView, FileDownloadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),  
    path('list/', FileListView.as_view(), name='file-list'), 
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file-download'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
