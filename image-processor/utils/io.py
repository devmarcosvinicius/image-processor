from skimage.io import imread, imsave


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
