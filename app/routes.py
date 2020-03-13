import os
import tarfile
import zipfile

from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User, Service
from datetime import datetime
from flask import flash, redirect, render_template, \
    request, send_from_directory, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


def run_protoc(service_name, version):
    os.system(
        f'/usr/local/bin/protoc \
            /googleapis/google/cloud/{service_name}/{version}/*.proto \
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

    Arguments:
        client_directory {string} -- location of files to add to the tarball
        target_directory {string} -- location to save the created tarball
    '''
    os.chdir(output_directory)
    t = tarfile.open('client.tar.gz', mode='w:gz')
    t.add(client_directory, arcname='cloud-run-client')
    t.close()


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Home',
        user=current_user,
        services=Service.query.all()
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    '''Logs out current user.

    Returns:
        Flask.redirect -- redirects to 'index'
    '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Registers new user.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    events = user.events
    return render_template('user.html', user=user, events=events)


@app.route('/edit_profile')
@login_required
def edit_profile():
    form = EditProfileForm()
    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form
    )


@app.route('/input')
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
@login_required
def generate_client():
    '''Generates client library, creates a tarball containing
    the source code and downloads it.

    Raises:
        GeneratorError -- on failure to generate client.

    Returns:
        Flask.redirect -- redirects on success.
    '''
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
    run_protoc('vision', 'v1')

    # create tar ball for download
    print(f'Client temp directory: {app.config["CLIENT_DIR"]}', flush=True)
    print(f'Download temp directory: {app.config["DOWNLOAD_DIR"]}', flush=True)
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
@login_required
def download():
    return send_from_directory(
            directory=app.config['DOWNLOAD_DIR'],
            mimetype='application/gzip',
            filename='client.tar.gz',
            as_attachment=True
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
