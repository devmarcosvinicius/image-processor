import processing.matrix as matrix
import utils.io as io
import processing.combination as combination
import utils.plot as plt


def menu() -> str:
    return """
1. Gerar uma matriz em Excel de uma imagem.
2. Cores da Imagem.
3. Encontrar diferença entre duas imagens.
4. Transferir histograma entre duas imagens.
5. Mostrar Imagem
0. Sair.
"""


if __name__ == "__main__":
    while True:
        print(menu())
        option = input("O que deseja fazer? ")

        match option:
            case "0":
                break
            case "1":
                image_path = input("Digite o caminho da imagem: ")
                write_coordinates = input("Você gostaria de adicionar as coordenadas? (s/n): ").lower()
                write_coordinates = True if write_coordinates == "s" else False
                output_path = input("Digite o caminho com o nome do arquivo: (Ex. "
                                    "C:\\Users\\User\\Images\\Imagem-em-exel)") + ".xlsx"

                matrix.write_image_in_excel(image_path, output_path, write_coordinates)
                print("O arquivo Excel foi gerado com sucesso.")
            case "2":
                image_path = input("Digite o caminho da imagem: ")
                print(matrix.get_image_colors(image_path))
            case "3":
                image_path_1 = input("Digite o caminho da primeira imagem: ")
                image_1 = io.imread(image_path_1)

                image_path_2 = input("Digite o caminho da segunda imagem: ")
                image_2 = io.imread(image_path_2)

                result = combination.find_difference(image_1, image_2)
                plt.plot_result(result)
            case "4":
                image_path_1 = input("Digite o caminho da primeira imagem: ")
                image_1 = io.imread(image_path_1)

                image_path_2 = input("Digite o caminho da segunda imagem: ")
                image_2 = io.imread(image_path_2)

                result = combination.transfer_histogram(image_1, image_2)
                plt.plot_result(result)
            case "5":
                image_path_1 = input("Digite o caminho da primeira imagem: ")
                image_1 = io.imread(image_path_1)
                plt.plot_image(image_1)
            case _:
                print("Opção invalida. Tente novamente.")
