import numpy
from skimage.transform import resize
from skimage.transform import rescale
from skimage import exposure
from skimage import util


def rescale_image(image, proportion):
    return rescale(image, proportion)


def resize_image(image, new_size: str):
    # assert 0 <= proportion <= 1, "Specify a valid proportion between 0 and 1."
    height, width = map(str.strip, new_size.split(","))
    height = float(height)
    width = float(width)

    new_size = tuple(new_size)
    new_size = (height, width)

    return resize(image, new_size)


def flip_image_horizontally(image):
    return image[:, ::-1, ...]


def flip_image_vertically(image):
    return image[::-1, :, ...]


def mirror_image(image):
    flipped_image = flip_image_horizontally(image)

    return numpy.hstack([image, flipped_image])


def change_contrast(image, contrast_level):
    return exposure.adjust_gamma(image, gamma=contrast_level)


def change_brightness(image, brightness_level):
    image_float = util.img_as_float(image)
    adjusted_image = image_float * brightness_level

    return exposure.adjust_gamma(adjusted_image)
