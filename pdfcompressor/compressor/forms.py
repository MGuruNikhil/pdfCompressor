from django import forms
from .models import CompressedPDF

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = CompressedPDF
        fields = ['original_pdf']