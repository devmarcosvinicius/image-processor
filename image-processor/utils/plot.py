import matplotlib.pyplot as plt


def plot_image(image):
    """
    Plota uma imagem em escala de cinza.

    Parâmetros:
    image (numpy.ndarray): A imagem a ser plotada.

    Retorna:
    None
    """
    plt.figure(figsize=(12, 4))
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()


def plot_result(*args):
    """
    Plota imagens em uma única linha, cada uma com um título correspondente.

    Parâmetros:
    *args (numpy.ndarray): Uma ou mais imagens a serem plotadas.

    Retorna:
    None
    """
    number_images = len(args)
    fig, axis = plt.subplots(nrows=1, ncols=number_images, figsize=(12, 4))
    names_lst = ['Image {}'.format(i) for i in range(1, number_images+1)]

    for ax, name, image in zip(axis, names_lst, args):
        ax.set_title(name)
        ax.imshow(image, cmap='gray')
        ax.axis('off')

    fig.tight_layout()
    plt.show()


def plot_histogram(image):
    """
    Plota o histograma de uma imagem em cada canal de cor.

    Parâmetros:
    image (numpy.ndarray): A imagem cujo histograma será plotado.

    Retorna:
    None
    """
    fig, axis = plt.subplots(nrows=1, ncols=3, figsize=(12, 4), sharex=True, sharey=True)
    color_lst = ['red', 'green', 'blue']

    for index, (ax, color) in enumerate(zip(axis, color_lst)):
        ax.set_title('{} histogram'.format(color.title()))
        ax.hist(image[:, :, index].ravel(), bins=256, color=color, align='mid')

    fig.tight_layout()
    plt.show()
