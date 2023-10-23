from django import forms

class PDFUploadForm(forms.Form):
    original_pdf = forms.FileField(label="Choose a PDF file")