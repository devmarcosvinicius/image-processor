import numpy
import numpy as np
from skimage.io import imread, imsave
from PyQt5.QtGui import QPixmap, QImage


def read_image(image):
    """
    Lê uma imagem de um arquivo.

    Parâmetros:
    image (str): O caminho para o arquivo de imagem a ser lido.

    Retorna:
    numpy.ndarray: A imagem lida.
    """
    image = imread(image)
    return image


def save_image(output, image):
    """
    Salva uma imagem em um arquivo.

    Parâmetros:
    output (str): O caminho para o arquivo de saída.
    image (numpy.ndarray): A imagem a ser salva.

    Retorna:
    None
    """
    imsave(output, image, format='PNG')


def image_to_qpixmap(image: np.ndarray) -> QPixmap:
    """
    Converte uma imagem no formato numpy.ndarray para QPixmap.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser convertida.

    Retorna:
    QPixmap: A imagem convertida para QPixmap.
    """
    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8)  # Convert float image to uint8

    if len(image.shape) == 3:
        if image.shape[2] == 3:
            format = QImage.Format_RGB888
        elif image.shape[2] == 4:
            format = QImage.Format_RGBA8888
    else:
        format = QImage.Format_Grayscale8

    height, width, channels = image.shape
    bytes_per_line = channels * width
    qimage = QImage(image.data, width, height, bytes_per_line, format)
    qpixmap = QPixmap.fromImage(qimage.rgbSwapped())  # Use rgbSwapped() to handle image correctly
    return qpixmap


def qpixmap_to_image(image: QPixmap) -> np.ndarray:
    """
    Converte um QPixmap em uma imagem numpy.ndarray.

    Parâmetros:
    qpixmap (QPixmap): O QPixmap a ser convertido.

    Retorna:
    numpy.ndarray: A imagem convertida como um array numpy.
    """
    image = image.toImage()
    image = np.frombuffer(image.constBits(), dtype=np.uint8).reshape(image.height(), image.width(), 4)
    return image.copy()
