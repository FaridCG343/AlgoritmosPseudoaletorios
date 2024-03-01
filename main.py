from PySide6.QtGui import QIcon

from views.MainMenu import MainWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Generador de números pseudoaleatorios")

    window = MainWindow()
    window.show()

    app.setWindowIcon(QIcon('img/random.ico'))

    sys.exit(app.exec())
