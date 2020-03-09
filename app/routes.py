import os
import sys
import tarfile
from werkzeug.utils import secure_filename
import zipfile

from app import app

from flask import Flask, request, send_from_directory


def run_protoc(service_name, version):
    os.system(
        f'/usr/local/bin/protoc /googleapis/google/cloud/{service_name}/{version}/*.proto \
            --proto_path={app.config["PATH_TO_API_COMMON_PROTOS"]} \
            --proto_path={app.config["GOOGLEAPIS"]} \
            --python_gapic_out={app.config["CLIENT_DIR"]}'
    )


def get_all_file_paths(directory):
    '''Returns list of paths to each file in a passed directory

    Args:
        directory: absolute path to a directory

    Returns:
        List of absolute paths to all files in the directory
        and its descendent directories
    '''
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


def create_tarball(client_directory, output_directory):
    '''Creates a tarball from generated client files

    Args:
        target_directory: location to save the created tarball
    '''
    os.chdir(output_directory)
    t = tarfile.open('client.tar.gz', mode='w:gz')
    t.add(client_directory, arcname='cloud-run-client')
    t.close()


@app.route('/')
@app.route('/index')
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

    if not in_file:
        return "No file"

    in_file_name = secure_filename(in_file.filename)
    in_file_path = os.path.join(app.config['UPLOAD_DIR'], in_file_name)
    in_file.save(in_file_path)

    # check file safety??
    # check type of uploaded file is tar or zip and extract

    if tarfile.is_tarfile(in_file_path):
        tf_in = tarfile.open(in_file_path, mode='r:gz')
        tf_in.extractall(path=app.config['PROTO_DIR'])
    elif zipfile.is_zipfile(in_file_path):
        zf_in = zipfile.ZipFile(in_file, 'r')
        zf_in.extractall(path=app.config['PROTO_DIR'])
    else:
        return """
        <html>
            <body>
                <h1>Not a valid file.</h1>
                <p>Please upload tar.gz or zip only.</p>
            </body>
        </html>
        """

    # call protoc (with gapic plugin) on the uploaded directory
    run_protoc('vision','v1')

    # create tar ball for download
    print(f'Client temp directory: {app.config["CLIENT_DIR"]}', flush=True)
    print(f'Output temp directory: {app.config["DOWNLOAD_DIR"]}', flush=True)
    create_tarball(app.config["CLIENT_DIR"], app.config["DOWNLOAD_DIR"])

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
def download():
    print(f'Sending from {app.config}', flush=True)
    return send_from_directory(
            directory=app.config["DOWNLOAD_DIR"],
            filename='./client.tar.gz',
            as_attachment=True
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
