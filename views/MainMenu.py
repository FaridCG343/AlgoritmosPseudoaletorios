from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Menu')

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.new_game_button = QPushButton('New Game')
        layout.addWidget(self.new_game_button)

        self.load_game_button = QPushButton('Load Game')
        layout.addWidget(self.load_game_button)

        self.quit_button = QPushButton('Quit')
        layout.addWidget(self.quit_button)

        self.show()
