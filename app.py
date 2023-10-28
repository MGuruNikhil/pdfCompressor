from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import io 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_pdf():
    if 'file' not in request.files:
        return "no file there, u idiot >:("
    
    file = request.files['file']

    output_name = request.form['output_name'] + ".pdf"

    if file.filename == '':
        return "select a file first, u idiot >:("

    if file:
        pdf = file.read()
        
        reader = PdfReader(io.BytesIO(pdf))
        writer = PdfWriter()

        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)

        # create BytesIO object -> store the compressed pdf
        compressed_pdf = io.BytesIO()
        writer.write(compressed_pdf)
        compressed_pdf.seek(0)  # reset the stream position

    return send_file(
        compressed_pdf,
        as_attachment = True,
        download_name = output_name
    )
if __name__ == '__main__':
    app.run(debug=True)
