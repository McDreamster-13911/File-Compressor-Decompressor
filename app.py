from flask import Flask, render_template, request, send_file
from compression_stuff import Tree
from decompress_stuff import build_huffman_tree, decode, decompress_binary_file
from tempfile import NamedTemporaryFile

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'doc', 'docx'}  # Add allowed file extensions

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
            # Get the content of the uploaded file
            file_content = file.read()

            # Process the file content using the Tree class
            tree = Tree()
            encoded_text = tree.encode(file_content)

            # Create a temporary file in memory without saving it
            with open('compressed.bin', 'wb') as temp_file:
                encoded_text.tofile(temp_file)

            # Return the compressed file to the user for download
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

        # Save the uploaded compressed file content to a temporary file
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)

        # Build Huffman tree from the compressed file content
        tree_root = build_huffman_tree(file_content)

        # Decompress the uploaded file
        decompressed_file_path = 'decompressed.txt'
        decompress_binary_file(temp_file.name, decompressed_file_path, tree_root)

        # Return the decompressed file to the user for download
        return send_file(decompressed_file_path, as_attachment=True, download_name='decompressed.txt', mimetype='text/plain', cache_timeout=0)

    return render_template('decompress.html')


