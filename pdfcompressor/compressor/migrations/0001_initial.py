# Generated by Django 4.2.5 on 2023-10-02 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompressedPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_pdf', models.FileField(upload_to='uploads/')),
                ('compressed_pdf', models.FileField(upload_to='compressed/')),
            ],
        ),
    ]
