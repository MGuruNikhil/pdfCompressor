from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PDFUploadForm
from .models import CompressedPDF
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
            compressed_pdf_path = 'compressed/' + original_pdf.name

            with open(compressed_pdf_path, 'wb') as output_file:
                compressed_pdf.write(output_file)

            instance = CompressedPDF(original_pdf=original_pdf, compressed_pdf=compressed_pdf_path)
            instance.save()
            return redirect('download', pk=instance.pk)
    else:
        form = PDFUploadForm()
    return render(request, 'compressor/index.html', {'form': form})

def download_compressed_pdf(request, pk):
    compressed_pdf = CompressedPDF.objects.get(pk=pk)
    file_path = compressed_pdf.compressed_pdf.path
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response
