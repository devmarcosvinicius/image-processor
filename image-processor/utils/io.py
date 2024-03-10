from skimage.io import imread, imsave


def read_image(path, is_gray=False):
    image = imread(path, as_grey=is_gray)
    return image


def save_image(path, image):
    imsave(path, image)
