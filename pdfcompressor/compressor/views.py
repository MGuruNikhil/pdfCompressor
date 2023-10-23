from django.shortcuts import render
from django.http import HttpResponse
from .forms import PDFUploadForm
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
            compressed_pdf_name = form.cleaned_data.get('compressed_pdf_name', 'compressed.pdf')

            if compressed_pdf_name[-4:] != ".pdf":
                compressed_pdf_name += ".pdf"

            # Create the response to serve the compressed PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{compressed_pdf_name}"'

            # Write the compressed PDF content to the response
            output_pdf_stream = io.BytesIO()
            compressed_pdf.write(output_pdf_stream)
            response.write(output_pdf_stream.getvalue())

            return response
    else:
        form = PDFUploadForm()
    
    return render(request, 'compressor/index.html', {'form': form})
    