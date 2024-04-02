from skimage.io import imread


def is_valid_image_path(image_path: str) -> bool:
    try:
        imread(image_path)
        return True

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{image_path}'.")
        return False

    except Exception as e:
        print(f"Erro: Falha ao ler a imagem em '{image_path}'.")
        print(e)
        return False


def get_image_path():
    image_path = input("Digite o caminho da imagem: ")
    while not is_valid_image_path(image_path):
        image_path = input("Caminho inválido. Digite novamente o caminho da primeira imagem: ")

    # image = imread(image_path)

    return image_path


def get_images_path():
    image_path_1 = input("Digite o caminho da primeira imagem: ")
    while not is_valid_image_path(image_path_1):
        image_path_1 = input("Caminho inválido. Digite novamente o caminho da primeira imagem: ")

    # image_1 = imread(image_path_1)

    image_path_2 = input("Digite o caminho da segunda imagem: ")
    while not is_valid_image_path(image_path_2):
        image_path_2 = input("Caminho inválido. Digite novamente o caminho da segunda imagem: ")

    # image_2 = imread(image_path_2)

    return image_path_1, image_path_2


def is_valid_contrast_level(factor: float) -> bool:
    if not isinstance(factor, float):
        print("Erro: O fator de contraste deve ser um numero.")
        return False

    if factor <= 0.0:
        print("Erro: O fator de contraste deve ser maior que zero.")
        return False

    return True


def is_valid_brightness_level(level: float) -> bool:
    if not isinstance(level, float):
        print("Erro: O nivel de brilho deve ser um numero.")
        return False

    if level < 0.0:
        print("Erro: O nivel do brilho deve estar entre 0.0 e 1.0.")
        return False

    return True


def get_contrast_level() -> float:
    contrast_level = float(input(f"""
O Valor deve ser igual ou maior que 0.
O valor 1 é o contraste original da imagem.
Valores maior do que 1 iram aumentar o contraste da imagem.
Digite o valor do contraste: """))

    while not is_valid_contrast_level(contrast_level):
        contrast_level = float(input(f"""
Valor invalido.
O Valor deve ser igual ou maior que 0.
O valor 1 é o contraste original da imagem.
Valores maior do que 1 iram aumentar o contraste da imagem.
Digite novamente. Digite o valor do contraste: """))

    return contrast_level


def get_brightness_level() -> float:
    brightness_level = float(input(f"""
O Valor deve ser igual ou maior que 0.
O valor 1 é o contraste original da imagem.
Valores maior do que 1 iram aumentar o brilho da imagem.
Digite o valor do brilho: """))

    while not is_valid_brightness_level(brightness_level):
        brightness_level = float(input(f"""
Valor invalido.
O Valor deve ser igual ou maior que 0.
O valor 1 é o contraste original da imagem.
Valores maior do que 1 iram aumentar o brilho da imagem.
Digite novamente. Digite o valor do brilho: """))

    return brightness_level
