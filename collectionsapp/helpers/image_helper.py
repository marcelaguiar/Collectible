from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ExifTags


def generate_thumbnail(i):
    # Takes in an ImageFieldField
    square_edge_length = 200
    target_width = square_edge_length
    target_height = square_edge_length

    left = 0
    top = 0
    right = target_width
    bottom = target_height

    im = Image.open(i)

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
        # cases: image don't have getexif
        pass

    # get new dimensions to fit
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
        im.thumbnail([new_width, new_height], Image.ANTIALIAS)
    else:
        im = im.resize((new_width, new_height))

    # crop
    if new_width > target_width:
        left = int((new_width - target_width) / 2)
        right = left + target_width
    elif new_height > target_height:
        top = int((new_height - target_height) / 2)
        bottom = top + target_height

    im = im.crop((left, top, right, bottom))

    buffer = BytesIO()
    im.save(fp=buffer, format='JPEG', quality=95)

    return ContentFile(buffer.getvalue())
