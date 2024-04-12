
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


def rgba_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Converte uma imagem no formato RGBA para RGB.

    Parâmetros:
    image (numpy.ndarray): A imagem RGBA a ser convertida.

    Retorna:
    numpy.ndarray: A imagem convertida para RGB.
    """
    return image[:, :, :3]  # Mantém apenas os canais RGB


def image_to_qpixmap(image: np.ndarray) -> QPixmap:
    """
    Converte uma imagem no formato numpy.ndarray para QPixmap.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser convertida.

    Retorna:
    QPixmap: A imagem convertida para QPixmap.
    """
    # Normalizar os valores de pixel para o intervalo [0, 255]
    image_normalized = (image - np.min(image)) * (255.0 / (np.max(image) - np.min(image)))
    image_normalized = image_normalized.astype(np.uint8)

    if len(image_normalized.shape) == 3:
        if image_normalized.shape[2] == 3:
            qformat = QImage.Format_RGB888
        elif image_normalized.shape[2] == 4:
            qformat = QImage.Format_RGBA8888
    else:
        qformat = QImage.Format_Grayscale8

    height, width, channels = image_normalized.shape
    bytes_per_line = channels * width
    qimage = QImage(image_normalized.data, width, height, bytes_per_line, qformat)
    qpixmap = QPixmap.fromImage(qimage.rgbSwapped())  # Use rgbSwapped() to handle image correctly
    return qpixmap


