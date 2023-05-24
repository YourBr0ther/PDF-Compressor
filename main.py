from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def compress_pdf(input_file_path, output_file_path):
    quality = '/screen'
    output_file_path = output_file_path if output_file_path else input_file_path.replace('.pdf', '_compressed.pdf')

    if not os.path.isfile(output_file_path):
        subprocess.call(['gswin64c', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS={}'.format(quality), '-dEmbedAllFonts=true', '-dSubsetFonts=true', '-dAutoRotatePages=/None', '-dDownsampleColorImages=true', '-dColorImageDownsampleType=/Bicubic', '-dColorImageResolution=150', '-dGrayImageDownsampleType=/Bicubic', '-dGrayImageResolution=150', '-dMonoImageDownsampleType=/Bicubic', '-dMonoImageResolution=150', '-dNOPAUSE', '-dBATCH', '-sOutputFile={}'.format(output_file_path), input_file_path])

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return 'No file part'
        file = request.files['pdf']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.pdf', '_compressed.pdf'))
            compress_pdf(input_file, output_file)
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename.replace('.pdf', '_compressed.pdf'), as_attachment=True)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
