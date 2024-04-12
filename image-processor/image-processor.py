from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic

from PIL import Image

import processing.matrix as matrix
import processing.transformation as transformation
import utils.io as io


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.loaded_image_path = None
        self.loaded_image = None
        uic.loadUi("form.ui", self)

        # Conectar os botões aos métodos correspondentes
        self.matrix_button.clicked.connect(self.generate_excel_matrix)
        self.matrix_colors_button.clicked.connect(self.get_image_colors)
        self.contrast_button.clicked.connect(self.adjust_contrast)
        self.brightness_button.clicked.connect(self.adjust_brightness)
        self.mirror_button.clicked.connect(self.mirror_image)
        self.rotate_horizontally_button.clicked.connect(self.rotate_horizontally)
        self.rotate_vertically_button.clicked.connect(self.rotate_vertically)
        self.scale_button.clicked.connect(self.change_scale)
        self.save_button.clicked.connect(self.save_image)
        self.load_image_button.clicked.connect(self.load_image)
        self.leave_button.clicked.connect(self.close)

        self.show()

    def load_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Abrir Imagem')
        file_dialog.setNameFilter('Images (*.png *.jpg *.bmp)')
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(file_path)
            self.loaded_image = pixmap
            if not pixmap.isNull():
                self.loaded_image_path = file_path  # Save the file path
                self.loaded_image = io.read_image(self.loaded_image_path)  # Open the image with Pillow
                self.display_image(pixmap)  # Display the image in the QLabel
            else:
                QMessageBox.warning(self, 'Option Clicked', 'Arquivo invalido.')
                return

    def display_image(self, pixmap):
        # Remove any existing image from the QLabel
        self.image_label.clear()
        # Set the pixmap as the image in the QLabel
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def generate_excel_matrix(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return

        self.loaded_image = Image.open(self.loaded_image_path)
        coordinates = QMessageBox.question(self, 'Coordenadas', 'Você deseja mostrar as coordenadas das cores '
                                                                'na matriz?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        show_coordinates = coordinates == QMessageBox.Yes
        output_file_path, _ = QFileDialog.getSaveFileName(self, 'Salvar Matriz no Arquivo Excel', '',
                                                          'Excel files (*.xlsx)')

        if output_file_path:
            matrix.write_image_in_excel(self.loaded_image, output_file_path, show_coordinates)
            QMessageBox.warning(self, 'Sucesso', 'Matriz gerada em um arquivo Excel.')

    def get_image_colors(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return

        dicionario = matrix.get_image_colors(self.loaded_image)

        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Salvar Cores')
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter('Text files (*.txt)')
        file_dialog.setDefaultSuffix('txt')

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, 'w') as f:
                for key, value in dicionario.items():
                    f.write(f"{key}: {value}\n")

            QMessageBox.warning(self, 'Sucesso', 'Cores salvas com sucesso.')

    def adjust_contrast(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return

        value, ok = QInputDialog.getDouble(self, 'Ajuste de Contraste', 'Digite o valor de contraste:', 0.0, 0.0)
        if ok:
            self.loaded_image = transformation.change_contrast(self.loaded_image, value)
            result_pixmap = io.image_to_qpixmap(self.loaded_image)
            self.display_image(result_pixmap)

    def adjust_brightness(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return

        value, ok = QInputDialog.getDouble(self, 'Ajuste de Contraste', 'Digite o valor do brilho:', 0.0, 0.0)
        if ok:
            self.loaded_image = transformation.change_brightness(self.loaded_image, value)
            result_pixmap = io.image_to_qpixmap(self.loaded_image)
            self.display_image(result_pixmap)

    def mirror_image(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return
        self.loaded_image = transformation.mirror_image(self.loaded_image)
        result_pixmap = io.image_to_qpixmap(self.loaded_image)
        self.display_image(result_pixmap)

    def rotate_horizontally(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return
        self.loaded_image = transformation.flip_image_horizontally(self.loaded_image)
        result_pixmap = io.image_to_qpixmap(self.loaded_image)
        self.display_image(result_pixmap)

    def rotate_vertically(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return
        self.loaded_image = transformation.flip_image_vertically(self.loaded_image)
        result_pixmap = io.image_to_qpixmap(self.loaded_image)
        self.display_image(result_pixmap)

    def change_scale(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return

        value, ok = QInputDialog.getDouble(self, 'Ajuste de Contraste', 'Digite o valor da escala:', 0.0, 0.0)
        if ok:
            self.loaded_image = transformation.rescale_image(self.loaded_image, value)
            # result_pixmap = io.image_to_qpixmap(self.loaded_image)
            self.display_image(self.loaded_image)

    def save_image(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return

        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Salvar Imagem')
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter('Images (*.png *.jpg *.bmp)')
        file_dialog.setDefaultSuffix('png')

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            io.save_image(file_path, self.loaded_image)
            QMessageBox.warning(self, 'Sucesso', 'Imagem salva com sucesso.')


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()
