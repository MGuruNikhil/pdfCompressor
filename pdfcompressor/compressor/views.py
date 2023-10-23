from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PDFUploadForm
from django.conf import settings
import PyPDF2
import io

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

            # Create the response to serve the compressed PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="compressed.pdf"'

            # Write the compressed PDF content to the response
            output_pdf_stream = io.BytesIO()
            compressed_pdf.write(output_pdf_stream)
            response.write(output_pdf_stream.getvalue())

            return response
    else:
        form = PDFUploadForm()
    
    return render(request, 'compressor/index.html', {'form': form})
    