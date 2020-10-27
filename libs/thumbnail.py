from PIL import Image, UnidentifiedImageError


def create_thumbnail(file_type, **kwargs) -> bool:
    if file_type == 'image':
        return create_image_thumbnail(**kwargs)


def create_image_thumbnail(source_path: str, destination_path: str) -> bool:
    # noinspection PyBroadException
    try:
        image = Image.open(source_path)
        resolution_320p = (352, 240)
        image.thumbnail(resolution_320p)
        image.save(destination_path)
        return True
    except UnidentifiedImageError:
        return False
    except Exception as e:
        from .. import logger
        logger.warning('Image thumbnail creation failed: ' + e)
        return False
