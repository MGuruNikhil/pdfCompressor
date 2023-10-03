from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PDFUploadForm
from .models import CompressedPDF
from django.conf import settings
import PyPDF2
import os

def compress_pdf(pdf_file):
    output_pdf = PyPDF2.PdfWriter()
    input_pdf = PyPDF2.PdfReader(pdf_file)

    for page_num in range(len(input_pdf.pages)):
        page = input_pdf.pages[page_num]
        page.compress_content_streams()
        output_pdf.add_page(page)

    return output_pdf

def index(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            original_pdf = form.cleaned_data['original_pdf']
            compressed_pdf = compress_pdf(original_pdf)
            compressed_pdf_name = 'compressed_' + original_pdf.name

            # Define the target directory for compressed PDFs
            target_directory = os.path.join(settings.MEDIA_ROOT, 'compressed')

            # Create the target directory if it doesn't exist
            os.makedirs(target_directory, exist_ok=True)

            # Create the full path for the compressed PDF
            compressed_pdf_path = os.path.join(target_directory, compressed_pdf_name)

            with open(compressed_pdf_path, 'wb') as output_file:
                compressed_pdf.write(output_file)

            instance = CompressedPDF(original_pdf=original_pdf, compressed_pdf=compressed_pdf_path)
            instance.save()
            return redirect('download', pk=instance.pk)
    else:
        form = PDFUploadForm()
    
    compressed_pdf = None
    return render(request, 'compressor/index.html', {'form': form, 'compressed_pdf': compressed_pdf})

def download_compressed_pdf(request, pk):
    compressed_pdf = CompressedPDF.objects.get(pk=pk)
    file_path = compressed_pdf.compressed_pdf.path
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response
