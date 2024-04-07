from skimage.io import imread, imsave


def read_image(image):
    image = imread(image)
    return image


def save_image(output, image):
    imsave(output, image, format='PNG')
