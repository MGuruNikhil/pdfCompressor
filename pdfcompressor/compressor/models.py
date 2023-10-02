from django.db import models

class CompressedPDF(models.Model):
    original_pdf = models.FileField(upload_to='uploads/')
    compressed_pdf = models.FileField(upload_to='compressed/')