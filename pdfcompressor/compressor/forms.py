from django import forms
from django.core.validators import FileExtensionValidator

class PDFUploadForm(forms.Form):
    original_pdf = forms.FileField(
        label="Choose a PDF file",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    compressed_pdf_name = forms.CharField(label="Compressed PDF Name", required=False)