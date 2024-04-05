from skimage.io import imread, imsave


def read_image(image, is_gray=False):
    image = imread(image, as_grey=is_gray)
    return image


def save_image(output, image):
    imsave(output, image, format='PNG')
