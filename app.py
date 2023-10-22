from flask import Flask, render_template, request, send_file
import PyPDF2
import io 
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_pdf():
    if 'file' not in request.files:
        return "no file there, u idiot >:("
    
    file = request.files['file']

    if file.filename == '':
        return "select a file first, u idiot >:("

    if file:
        pdf = file.read()
        return "yayy, yes file there"

if __name__ == '__main__':
    app.run(debug=True)
