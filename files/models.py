from django.db import models
from django.conf import settings  # Import settings to access the user model
from django.contrib.auth import get_user_model

User = get_user_model()


class File(models.Model):
    file_name = models.CharField(max_length=255, default="default_files") 
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=[('pptx', 'PPTX'), ('docx', 'DOCX'), ('xlsx', 'XLSX') ,  ('pdf', 'PDF')], default='pptx')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_upload_file", "Can upload file"),
            ("can_download_file", "Can download file"),
            ("can_see_files_list", "Can see the list of all files"),
        ]

    def __str__(self):
        return self.file_name
