# Generated by Django 5.2 on 2025-04-25 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_alter_file_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'permissions': [('can_upload_file', 'Can upload file'), ('can_download_file', 'Can download file'), ('can_see_files_list', 'Can see the list of all files')]},
        ),
    ]
