from rest_framework import serializers
from .models import File

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'file', 'file_type' ]

    def validate_file(self, value):
        allowed_types = {
            'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'pdf': 'application/pdf',
        }

        # Check if the file's content type is one of the allowed types
        file_extension = value.name.split('.')[-1]  
        if file_extension not in allowed_types:
            raise serializers.ValidationError('File type not allowed. Only pptx, docx, and xlsx are allowed.')

        # Set the file type based on the file's extension
        value.file_type = file_extension  
        return value

    def create(self, validated_data):
        # Add the current user to the validated data before saving the file
        validated_data['uploaded_by'] = self.context['request'].user  
        return super().create(validated_data)
