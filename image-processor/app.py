import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, \
    QGridLayout, QInputDialog, QLineEdit, QSlider, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from PIL import Image

from processing import matrix
from processing import transformation
from utils import io
from utils import plot as plt


class ImageLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.loaded_image_path = None
        self.button_options = None
        self.label = None
        self.button_load = None
        self.loaded_image = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(300, 200)

        self.button_load = QPushButton('Carregar Imagem', self)
        self.button_load.clicked.connect(self.load_image)

        self.button_options = {
            'matrix_to_excel': QPushButton('Gerar uma matriz em Excel', self),
            'image_colors': QPushButton('Cores da Imagem', self),
            'images_differences': QPushButton('Diferença entre imagens', self),
            'exchange_histogram_between_images': QPushButton('Transferir histograma', self),
            'change_contrast': QPushButton('Ajuste de Contraste', self),
            'change_brightness': QPushButton('Ajuste de Brilho', self),
            'invert_side': QPushButton('Inverter lado', self),
            'mirror_image': QPushButton('Espelhar imagem', self),
            'resize': QPushButton('Resize', self),
            'leave': QPushButton('Sair', self)
        }

        for option, button in self.button_options.items():
            button.clicked.connect(lambda _, opt=option: self.on_option_clicked(opt))
            button.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_load)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.button_options['matrix_to_excel'], 0, 0)
        grid_layout.addWidget(self.button_options['image_colors'], 1, 0)
        grid_layout.addWidget(self.button_options['change_contrast'], 0, 1)
        grid_layout.addWidget(self.button_options['change_brightness'], 1, 1)
        grid_layout.addWidget(self.button_options['images_differences'], 0, 2)
        grid_layout.addWidget(self.button_options['exchange_histogram_between_images'], 1, 2)
        grid_layout.addWidget(self.button_options['invert_side'], 0, 3)
        grid_layout.addWidget(self.button_options['mirror_image'], 1, 3)
        grid_layout.addWidget(self.button_options['resize'], 2, 3)

        layout.addLayout(grid_layout)
        layout.addWidget(self.button_options['leave'])

        self.setLayout(layout)
        self.loaded_image = None

    def load_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Abrir Imagem')
        file_dialog.setNameFilter('Images (*.png *.jpg *.bmp)')
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.loaded_image_path = file_path  # Save the file path
                self.loaded_image = io.read_image(self.loaded_image_path)  # Open the image with Pillow
                self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))
                self.button_load.hide()
                for button in self.button_options.values():
                    button.setVisible(True)
            else:
                self.label.setText('Arquivo Invalido.')

    def update_image(self):
        self.loaded_image = io.read_image(self.loaded_image_path)

    def on_option_clicked(self, option):
        match option:
            case "leave":
                self.close()

            case "matrix_to_excel":
                if self.loaded_image is None:
                    QMessageBox.warning(self, 'Option Clicked', 'No image loaded.')

                self.loaded_image = Image.open(self.loaded_image_path)
                coordinates = QMessageBox.question(self, 'Coordenadas', 'Você deseja mostrar as coordenadas das cores '
                                                                        'na matriz?',
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                show_coordinates = coordinates == QMessageBox.Yes
                output_file_path, _ = QFileDialog.getSaveFileName(self, 'Salvar Matriz no Arquivo Excel', '', 'Excel files (*.xlsx)')

                if output_file_path:
                    matrix.write_image_in_excel(self.loaded_image, output_file_path, show_coordinates)
                    QMessageBox.warning(self, 'Sucesso', 'Matriz gerada em um arquivo Excel.')

            case "image_colors":
                return

            case "mirror_image":
                if self.loaded_image is None:
                    QMessageBox.warning(self, 'Option Clicked', 'No image loaded.')
                    return

                contrast, ok = QInputDialog.getText(self, 'Contraste', 'Digite o valor do contraste:', QLineEdit.Normal)

                if ok:
                    contrast_value = float(contrast)

                    if contrast_value < 0 or contrast_value > 100:
                        QMessageBox.warning(self, 'Contraste inválido.', 'O contraste deve ser entre 0.0 e 100.')
                        return

                self.loaded_image = transformation.mirror_image(image=self.loaded_image)
                # self.update_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageLoader()
    window.show()
    sys.exit(app.exec_())
