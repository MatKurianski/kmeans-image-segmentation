from kmeans import kmeans as compress_image
import numpy as np

from PyQt5.QtWidgets import *
from PIL import Image

from os import path

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.main_layout = QVBoxLayout()
        self.path_input = QLineEdit()
        self.process_image_button = QPushButton('Process')
        self.colors_spinbox = QSpinBox()
        self.create_options_form()
        self.setLayout(self.main_layout)

        self.process_image_button.clicked.connect(self.on_process_button_click)
        self.main_layout.addWidget(self.process_image_button)
    
    def on_browse_button_click(self):
        image_path = self.search_image_path()
        self.path_input.setText(image_path)

    def on_process_button_click(self):
        image_path = self.path_input.text()
        if path.isfile(image_path) == False:
            self.display_alert('This file doesn\'t exist!')
            return
        
        colors = self.colors_spinbox.value()
        if colors <= 0:
            self.display_alert('The \'color\' value is invalid. Please, set a value higher than zero.')
            return
    
        image = self.load_image(image_path)
        width, height = image.size

        image_array = np.array(image).reshape(width * height, 3)

        centroids, idx = compress_image(image_array, self.colors_spinbox.value())

        new_image = Image.fromarray(centroids[idx].reshape(height, width, 3).astype(np.uint8))
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save file', image_path, "Image files (*.jpg *.jpeg *.png)")
        new_image.save(save_path)
        self.display_alert('Saved image as \'{}\'!'.format(save_path))
        self.done(0)
    
    def search_image_path(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './',"Image files (*.jpg *.jpeg *.png)")
        self.path_input.setText(fname)
        self.main_layout.addWidget(self.process_image_button)
        return fname

    def display_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()
    
    def load_image(self, path):
        return Image.open(path).convert('RGB')

    def create_options_form(self):
        options = QFormLayout()
        options.addRow(QLabel('Choose an image'))

        photo_chooser_layout = QHBoxLayout()
        photo_chooser_layout.addWidget(self.path_input)
        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.on_browse_button_click)
        photo_chooser_layout.addWidget(browse_button)

        options.addRow(photo_chooser_layout)
        options.addRow('Choose an maximum of colors', self.colors_spinbox)

        self.main_layout.addLayout(options)

