from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ExifTags
import copy


class ThumbnailSet:
    def __init__(self, i):
        # Takes in an ImageFieldField
        self.thumbnail, self.thumbnail_tiny = self._generate_thumbnail_set(i)

    @staticmethod
    def _generate_thumbnail_set(i):
        """Takes in an ImageFieldField and generates 2 different sized thumbnails: Thumbnail and Tiny thumbnail"""
        im = Image.open(i)

        # Apply exif rotation if it exists
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = im._getexif()

            if exif[orientation] == 3:
                im = im.rotate(180, expand=True)
            elif exif[orientation] == 6:
                im = im.rotate(270, expand=True)
            elif exif[orientation] == 8:
                im = im.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # cases: image doesn't have getexif
            pass

        pil_thumbnail = resize_image(im, 200)
        pil_thumbnail_tiny = resize_image(im, 100)

        thumbnail_buffer = BytesIO()
        thumbnail_buffer_tiny = BytesIO()

        pil_thumbnail.save(fp=thumbnail_buffer, format='JPEG', quality=95)
        pil_thumbnail_tiny.save(fp=thumbnail_buffer_tiny, format='JPEG', quality=95)

        thumbnail = ContentFile(thumbnail_buffer.getvalue())
        thumbnail_tiny = ContentFile(thumbnail_buffer_tiny.getvalue())

        return thumbnail, thumbnail_tiny


def resize_image(im, square_edge_length):
    target_width = square_edge_length
    target_height = square_edge_length

    # Calculate new dimensions to fit
    width, height = im.size
    if width > height:
        resize_ratio = target_height / height
        new_width = int(width * resize_ratio)
        new_height = target_height
    elif height > width:
        resize_ratio = target_width / width
        new_width = target_width
        new_height = int(height * resize_ratio)
    else:
        new_width = target_width
        new_height = target_height

    # grow or shrink to new dimensions
    if width >= target_width and height >= target_height:
        resized_image = copy.copy(im)  # TODO: Possibly use deepcopy?
        resized_image.thumbnail([new_width, new_height], Image.ANTIALIAS)
    else:
        resized_image = im.resize((new_width, new_height))

    # crop
    left = 0
    top = 0
    right = target_width
    bottom = target_height
    if new_width > target_width:
        left = int((new_width - target_width) / 2)
        right = left + target_width
    elif new_height > target_height:
        top = int((new_height - target_height) / 2)
        bottom = top + target_height

    cropped_image = resized_image.crop((left, top, right, bottom))

    return cropped_image
