"""
Gets and handles meta data from media files.
"""
from os import remove
from os.path import join, isfile

from flask import url_for
from magic import from_file

from .. import config
from .thumbnail import create_thumbnail

from webapi.libs.api.response import redirect_or_response


def get_thumbnail(file, ignore_cached=False):
    """
    Get the url to a thumbnail for a given file if possible, falling back to placeholder icons otherwise.

    File are searched within global media path and thumbnails are saved in the global thumbnail path.

    :param file: name of the file
    :param ignore_cached: if True, thumbnails are recreated even if they already exist
    :return: url for thumbnail
    """

    source_path = join(config.get('webapi', 'media_path'), file)
    thumb_path = join(config.get('webapi', 'thumbnail_path'), file)
    mime_type = from_file(source_path, mime=True)

    if mime_type.startswith('image/'):
        if not isfile(thumb_path) or ignore_cached:
            create_thumbnail('image', source_path=source_path, destination_path=thumb_path)
        if isfile(thumb_path):
            return url_for('get_thumbnail', filename=file)
        else:
            return url_for('.static', filename='icons/icon-65-document-image.svg')
    elif mime_type.startswith('video/'):
        return url_for('.static', filename='icons/icon-64-document-movie.svg')
    elif mime_type.startswith('audio/'):
        return url_for('.static', filename='icons/icon-63-document-music.svg')
    elif mime_type.startswith('text/'):
        return url_for('.static', filename='icons/icon-55-document-text.svg')
    else:
        return url_for('.static', filename='icons/icon-54-document.svg')


def remove_thumbnail(file: str):
    """
    Deletes a given file from the global thumbnail path if it exists.

    :param file: filename to delete
    :exception OSError: os.remove
    """

    thumb_path = join(config.get('webapi', 'thumbnail_path'), file)

    if isfile(thumb_path):
        remove(thumb_path)
