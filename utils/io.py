from PIL import Image


def read_image(image):
    image = Image.open(image.stream)
    return image
