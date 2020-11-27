"""
Routes for the files plugin.
"""
from os import remove as rm, listdir, rename as rn
from os.path import join, isdir, isfile
from pathlib import Path

from flask import render_template, request, flash, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import bp, config, logger
from .libs.meta import get_thumbnail
from webapi.libs.api.response import redirect_or_response


@bp.route('/', methods=['GET'])
@bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Renders the files dashboard.

    Arguments:
            - ignore_cached (optional), set to "1" or "True" to force recreation of all thumbnails.

    :return: rendered dashboard
    """

    ignore_cached_raw = request.args.get('ignore_cached') or "False"
    ignore_cached = True if ignore_cached_raw == "True" or ignore_cached_raw == "1" else False

    return render_template('files_dashboard.html', files=get_media_files(ignore_cached))


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """
    Saves an uploaded file to the media folder.

    :return: redirect or response
    """
    create_media_folder()

    if len(request.files) == 0:
        return redirect_or_response(400, 'No files argument')

    files = request.files.getlist('files')
    if not files or (len(files) == 1 and files[0].filename == ''):
        return redirect_or_response(400, 'Invalid files argument')

    for file in files:
        logger.info(f'Uploading file {file}')
        filename = secure_filename(file.filename)
        filepath = join(config.get('webapi', 'media_path'), filename)
        logger.debug(f'-> Saving location: {filepath}')
        file.save(filepath)
        logger.debug('-> File saved')

    return redirect_or_response(200, 'Success')


@bp.route('/remove', methods=['GET'])
@login_required
def remove():
    """
    Removes a file from the media folder.

    :return: redirect or response
    """
    create_media_folder()

    files = request.args.getlist('files')
    if not files or (len(files) == 1 and files[0] == ''):
        return redirect_or_response(400, 'Invalid files argument')

    for file in files:
        filename = secure_filename(file)
        filepath = join(config.get('webapi', 'media_path'), filename)
        if isfile(filepath):
            rm(filepath)
            logger.info(f'Deleted file {file}')
        else:
            logger.warning(f'File {file} not found. Deletion skipped')

    return redirect_or_response(200, 'Success')


@bp.route('/rename', methods=['GET'])
@login_required
def rename():
    """
    Rename a file in the media folder.

    :return: redirect or response
    """
    create_media_folder()

    old_name = request.args.get('old_name')
    new_name = request.args.get('new_name')

    if not old_name or old_name == '' or not new_name or new_name == '':
        return redirect_or_response(400, 'Missing new or old filename argument')

    old_name = secure_filename(old_name)
    new_name = secure_filename(new_name)

    old_fp = join(config.get('webapi', 'media_path'), old_name)
    new_fp = join(config.get('webapi', 'media_path'), new_name)

    if not isfile(old_fp):
        return redirect_or_response(400, 'File not found')

    if isfile(new_fp):
        return redirect_or_response(400, 'Name already taken')

    rn(old_fp, new_fp)

    return redirect_or_response(200, 'Success')


@bp.route('/list', methods=['GET'])
@login_required
def list_files():
    """
    Lists all files from the media folder.

    :return: json response containing all files as a list
    """
    create_media_folder()

    return jsonify(get_media_files())


def get_media_files(ignore_cached: bool = True):
    """
    Returns all files from the frameworks media folder.

    :return: list of tuples, every tuple contains the file and the thumbnail url
    """
    media_path = config.get('webapi', 'media_path')
    return [(f, get_thumbnail(f, ignore_cached)) for f in listdir(media_path) if isfile(join(media_path, f))]


def create_media_folder():
    """
    Creates the media folder. The media folder is using the frameworks media_path.

    :exception OSError: pathlib.Path.mkdir
    """
    if not isdir(config.get('webapi', 'media_path')):
        Path(config.get('webapi', 'media_path')).mkdir(parents=True, exist_ok=True)



