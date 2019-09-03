import sys

from window import MainWindow

from PyQt5.QtWidgets import QApplication

app = QApplication([])

window = MainWindow()
window.show()

sys.exit(app.exec_())
