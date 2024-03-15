import processing.matrix as matrix
import processing.combination as combination
import processing.transformation as transformation
import utils.io as io
import utils.plot as plt
import utils.validation as validation


def main_menu() -> str:
    return """
1. Gerar uma matriz em Excel de uma imagem.
2. Cores da Imagem.
3. Encontrar diferença entre duas imagens.
4. Transferir histograma entre duas imagens.
5. Ajuste de Contraste
6. Ajuste de Brilho
0. Sair.
"""


if __name__ == "__main__":
    while True:
        print(main_menu())
        option = input("O que deseja fazer? ")

        match option:
            case "0":
                break
            case "1":
                image_path = validation.get_image_path()
                write_coordinates = input("Você gostaria de adicionar as coordenadas? (s/n): ").lower()
                write_coordinates = True if write_coordinates == "s" else False
                output_path = input("Digite o caminho com o nome do arquivo: (Ex. "
                                    "C:\\Users\\User\\Images\\Imagem-em-exel)") + ".xlsx"

                matrix.write_image_in_excel(image_path, output_path, write_coordinates)
                print("O arquivo Excel foi gerado com sucesso.")

            case "2":
                image_path = validation.get_image_path()
                colors = matrix.get_image_colors(image_path)

                for name, coord in colors.items():
                    print(f"cor {name}: {coord}")

            case "3":
                image_1, image_2 = validation.get_images_path()

                result, g1, g2 = combination.find_difference(image_1, image_2)
                plt.plot_result(g1, g2, result)

            case "4":
                image_1, image_2 = validation.get_images_path()

                result = combination.transfer_histogram(image_1, image_2)
                plt.plot_result(image_1, image_2, result)

            # Contraste
            case "5":
                image = validation.get_image_path()

                contrast_level = validation.get_contrast_level()

                image = transformation.change_contrast(image, contrast_level)
                plt.plot_image(image)

            case "6":
                image = validation.get_image_path()
                brightness_level = validation.get_brightness_level()

                image = transformation.change_brightness(image, brightness_level)

                plt.plot_image(image)

            case _:
                print("Opção invalida. Tente novamente.")
