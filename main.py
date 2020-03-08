import os
import sys
import tarfile
import tempfile
from werkzeug.utils import secure_filename
import zipfile

from flask import Flask, request, send_from_directory

app = Flask(__name__)

PATH_TO_API_COMMON_PROTOS = '../api-common-protos/'
UPLOAD_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='./')
CLIENT_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='./')
PROTO_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='./')
TAR_DIR = tempfile.mkdtemp(prefix='/tmp/', dir='./')


def generate(proto_root_dir, path_to_protos):
    os.system(
        f'protoc {path_to_protos}/*.proto \
            --proto_path={PATH_TO_API_COMMON_PROTOS} \
            --proto_path={proto_root_dir} \
            --python_gapic_out={CLIENT_DIR}'
    )


'''
Function to find the likely location of the main proto file
Function returns the directory path of the first proto file it finds
while walking through
For this to work properly that first would need to import all others
required through accurate relative paths
'''


def get_path_to_protos(dir):
    for directory, _, files in os.walk(dir):
        for filename in files:
            filepath = os.path.join(directory, filename)
            if filepath.lower().endswith('.proto'):
                return directory


'''
Function returns a list of paths to each file in a passed directory
'''


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, _, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths


'''
Function creates a tarball from generated client files
'''


def mkTarFile():
    oldpath = os.getcwd()
    os.chdir(TAR_DIR)
    t = tarfile.open('client.tar.gz', mode='w:gz')
    for fname in get_all_file_paths(CLIENT_DIR):
        t.add(fname)
    t.close()
    os.chdir(oldpath)


@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1>Have yourself a client library:</h1>

                <form action="/generate" method="post"
                enctype="multipart/form-data">
                    <input type="file" name="proto_files" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """


@app.route('/generate', methods=["POST"])
def generate_client():
    # upload zip/tarball of files from web form
    in_file = request.files['proto_files']
    in_file_name = secure_filename(in_file.filename)
    in_file_path = os.path.join(UPLOAD_DIR, in_file_name)
    in_file.save(in_file_path)
    if not in_file:
        return "No file"

    # check file safety??
    # check type of uploaded file is tar or zip and extract

    if tarfile.is_tarfile(in_file_path):
        tf_in = tarfile.open(in_file_path, mode='r:gz')
        tf_in.extractall(path=PROTO_DIR)
    elif zipfile.is_zipfile(in_file_path):
        zf_in = zipfile.ZipFile(in_file, 'r')
        zf_in.extractall(path=PROTO_DIR)
    else:
        return "Not a valid tar file"

    # call protoc (with gapic plugin) on the uploaded directory
    # figure out how to construct the path strings that protoc needs
    generate(PROTO_DIR, get_path_to_protos(PROTO_DIR))
    # create tar ball for download
    mkTarFile()

    return """
        <html>
            <body>
                <h1>Success!</h1>
                <p>Your client awaits...</p>
                <body class="body">
                    <div class="container" align="left">
                        <a href="/download" target="blank">
                            <button>Download!</button></a>
                    </div>
                </body>
        </html>
    """


@app.route('/download', methods=["GET"])
def dlTarFile():
    return send_from_directory(
            directory=TAR_DIR,
            filename='client.tar.gz',
            mimetype='application/gzip',
            as_attachment=True
    )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', debug=True)
