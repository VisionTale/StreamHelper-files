"""
Creates thumbnails for various file formats.
"""
from os.path import isfile
from typing import Tuple

from PIL import Image, UnidentifiedImageError


def create_thumbnail(file_class, **kwargs) -> bool:
    """
    Create thumbnail based on the passed file_class argument.

    No assumptions are made within this function.

    Supported file classes are:
        - image

    :param file_class: file class to create thumbnail for.
    :param kwargs: arguments to pass to the specific thumbnail creation method
    :return: True if successful, False otherwise
    """
    if file_class == 'image':
        return create_image_thumbnail(**kwargs)
    return False


def create_image_thumbnail(source_path: str, destination_path: str, resolution: Tuple[int, int] = (352, 240)) -> bool:
    """
    Creates a thumbnail for an image file.

    :param source_path: file to create thumbnail for
    :param destination_path: file to save thumbnail to
    :param resolution: resolution of the thumbnail, first element is the width, second the height. Defaults to 320p.
    :return: True if successful, False otherwise
    """
    # noinspection PyBroadException
    try:
        image = Image.open(source_path)
        image.thumbnail(resolution)
        image.save(destination_path)
        if isfile(destination_path):
            return True
        from .. import logger
        logger.error('Image thumbnail creation finished, but file is still missing')
        return False
    except UnidentifiedImageError:
        return False
    except Exception as e:
        from .. import logger
        logger.warning('Image thumbnail creation failed: ' + e)
        return False
