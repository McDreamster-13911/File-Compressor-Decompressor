from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from compression_stuff import compress_file
from decompress_stuff import decompress_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['COMPRESSED_FOLDER'] = 'compressed/'
app.config['DECOMPRESSED_FOLDER'] = 'decompressed/'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/compress', methods=['GET', 'POST'])
def compress():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.txt'):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            output_filename = f"compressed_{filename}.bin"
            output_path = os.path.join(app.config['COMPRESSED_FOLDER'], output_filename)
            
            compression_ratio = compress_file(input_path, output_path)
            
            return render_template('compress.html', check=1, compression_ratio=compression_ratio, filename=output_filename)
    
    return render_template('compress.html', check=0)

@app.route('/decompress', methods=['GET', 'POST'])
def decompress():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.bin'):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
            file.save(input_path)
            
            output_filename = f"decompressed_{filename[11:-4]}.txt"
            output_path = os.path.join(app.config['DECOMPRESSED_FOLDER'], output_filename)
            
            decompressed_size = decompress_file(input_path, output_path)
            
            return render_template('decompress.html', check=1, decompressed_size=decompressed_size, filename=output_filename)
    
    return render_template('decompress.html', check=0)

@app.route('/download/<filename>')
def download(filename):
    if filename.startswith('compressed_'):
        return send_file(os.path.join(app.config['COMPRESSED_FOLDER'], filename), as_attachment=True)
    elif filename.startswith('decompressed_'):
        return send_file(os.path.join(app.config['DECOMPRESSED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DECOMPRESSED_FOLDER'], exist_ok=True)
    app.run(debug=True)

