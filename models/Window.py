from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic

import FaceDetector


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.loaded_image_path = None
        self.loaded_image = None
        uic.loadUi("form.ui", self)

        self.matrix_button.clicked.connect(self.image_face_detector)
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

    def image_face_detector(self):
        if self.loaded_image is None:
            QMessageBox.warning(self, 'Option Clicked', 'A imagem não foi carregada.')
            return

        face_detector = FaceDetector()
        face_detector.

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
