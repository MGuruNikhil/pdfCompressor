from django import forms

class PDFUploadForm(forms.Form):
    original_pdf = forms.FileField(label="Choose a PDF file")
    compressed_pdf_name = forms.CharField(label="Compressed PDF Name", required=False)