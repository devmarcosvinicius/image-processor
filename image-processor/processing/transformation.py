import numpy
from skimage.transform import resize
from skimage.transform import rescale
from skimage import exposure
from skimage import util


def rescale_image(image, proportion):
    """
    Redimensiona a imagem de acordo com a proporção fornecida.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser redimensionada.
    proportion (float): A proporção pela qual a imagem será redimensionada.

    Retorna:
    numpy.ndarray: A imagem redimensionada.
    """
    return rescale(image, proportion)


def resize_image(image, new_height: int, new_width: int):
    """
    Redimensiona a imagem para uma nova altura e largura especificadas.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser redimensionada.
    new_height (int): A nova altura da imagem.
    new_width (int): A nova largura da imagem.

    Retorna:
    numpy.ndarray: A imagem redimensionada.
    """
    return resize(image, (new_height, new_width), anti_aliasing=True)


def flip_image_horizontally(image):
    """
    Espelha a imagem horizontalmente.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser espelhada.

    Retorna:
    numpy.ndarray: A imagem espelhada horizontalmente.
    """
    return image[:, ::-1, ...]


def flip_image_vertically(image):
    """
    Espelha a imagem verticalmente.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser espelhada.

    Retorna:
    numpy.ndarray: A imagem espelhada verticalmente.
    """
    return image[::-1, :, ...]


def mirror_image(image):
    """
    Cria uma imagem espelhada horizontalmente, concatenando a imagem original com sua versão espelhada.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser espelhada.

    Retorna:
    numpy.ndarray: A imagem original concatenada com sua versão espelhada.
    """
    flipped_image = flip_image_horizontally(image)
    return numpy.hstack([image, flipped_image])


def move_image(image):
    """
    Move a imagem (ainda não implementado).

    Parâmetros:
    image (numpy.ndarray): A imagem a ser movida.

    Retorna:
    None
    """
    pass


def change_contrast(image, contrast_level):
    """
    Altera o contraste da imagem.

    Parâmetros:
    image (numpy.ndarray): A imagem cujo contraste será alterado.
    contrast_level (float): O nível de contraste a ser aplicado.

    Retorna:
    numpy.ndarray: A imagem com o contraste alterado.
    """
    return exposure.adjust_gamma(image, gamma=contrast_level)


def change_brightness(image, brightness_level):
    """
    Altera o brilho da imagem.

    Parâmetros:
    image (numpy.ndarray): A imagem cujo brilho será alterado.
    brightness_level (float): O nível de brilho a ser aplicado.

    Retorna:
    numpy.ndarray: A imagem com o brilho alterado.
    """
    image_float = util.img_as_float(image)
    adjusted_image = image_float * brightness_level

    return exposure.adjust_gamma(adjusted_image)