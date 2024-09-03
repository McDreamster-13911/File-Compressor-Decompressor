from flask import Flask, render_template, request, send_file
from compression_stuff import Tree
from decompress_stuff import build_huffman_tree, decode, decompress_binary_file
from tempfile import NamedTemporaryFile
import os

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'doc', 'docx'}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/compress', methods=['GET', 'POST'])
def compress():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('compress.html', error_message='No file selected.')

        file = request.files['file']

        if file.filename == '':
            return render_template('compress.html', error_message='No file selected.')

        if file and allowed_file(file.filename):
            file_content = file.read()
            tree = Tree()
            encoded_text = tree.encode(file_content.decode('utf-8'))

            with open('compressed.bin', 'wb') as temp_file:
                encoded_text.tofile(temp_file)

            return send_file('compressed.bin', as_attachment=True, download_name='compressed.bin', mimetype='application/octet-stream')

    return render_template('compress.html')

@app.route('/decompress', methods=['GET', 'POST'])
def decompress():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('decompress.html', error_message='No file selected.')

        file = request.files['file']

        if file.filename == '':
            return render_template('decompress.html', error_message='No file selected.')

        file_content = file.read()

        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            tree_root = build_huffman_tree(file_content)
            decompressed_file_path = 'decompressed.txt'
            decompress_binary_file(temp_file_path, decompressed_file_path, tree_root)

            # Return the decompressed file to the user for download
            return send_file(decompressed_file_path, as_attachment=True, download_name='decompressed.txt', mimetype='text/plain')
        finally:
            os.remove(temp_file_path)

    return render_template('decompress.html')

