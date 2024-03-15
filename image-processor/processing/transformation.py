from skimage.transform import resize
from skimage import exposure
from skimage import util


def resize_image(image, proportion):
    assert 0 <= proportion <= 1, "Specify a valid proportion between 0 and 1."

    height = round(image.shape[0] * proportion)
    width = round(image.shape[1] * proportion)
    image_resized = resize(image, (height, width), anti_aliasing=True)

    return image_resized


def change_contrast(image, contrast_level):
    return exposure.adjust_gamma(image, gamma=contrast_level)


def change_brightness(image, brightness_level):
    image_float = util.img_as_float(image)
    adjusted_image = image_float * brightness_level

    return exposure.adjust_gamma(adjusted_image)
