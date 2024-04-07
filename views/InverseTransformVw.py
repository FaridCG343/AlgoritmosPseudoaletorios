import matplotlib.pyplot
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QDoubleValidator
from PySide6.QtWidgets import (QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QGridLayout,
                               QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.Plots import plot_histogram, plot_scatter
from utils.InverseTransform import InverseTransform


class InverseTransformVw(QMainWindow):
    close_window = Signal()

    def __init__(self, data: list):
        super().__init__()

        self.data = data
        self.__InverseTransform = InverseTransform(data)
        self.setWindowTitle("Transformada Inversa")
        self.transformed_data = []

        # region Main layout
        # Main layout
        main_layout = QHBoxLayout()

        # Left side layout
        input_layout = QGridLayout()

        # Selector with methods from PseudoRandom class
        self.selector_label = QLabel("Selector")
        self.selector_combo = QComboBox()
        self.selector_combo.addItems(["Uniforme", "Exponencial"])
        input_layout.addWidget(self.selector_label, 0, 0)
        input_layout.addWidget(self.selector_combo, 0, 1)

        # Seed and parameters input
        self.a_label = QLabel("Ingrese a")
        self.a_input = QLineEdit()
        self.b_label = QLabel("Ingrese b")
        self.b_input = QLineEdit()

        # Add widgets to left layout
        input_layout.addWidget(self.a_label, 2, 0)
        input_layout.addWidget(self.a_input, 2, 1)
        input_layout.addWidget(self.b_label, 3, 0)
        input_layout.addWidget(self.b_input, 3, 1)

        # Generate button
        self.generate_button = QPushButton("Transformar")
        input_layout.addWidget(self.generate_button, 6, 0, 1, 2)

        # Left side layout
        left_layout = QVBoxLayout()
        left_layout.addLayout(input_layout)
        left_layout.addStretch()  # This will push the grid layout to the top

        self.plot_selector_label = QLabel("Seleccione el tipo de gráfico:")
        self.plot_selector_combo = QComboBox()
        self.plot_selector_combo.addItems(["Histograma", "Dispersión"])
        left_layout.addWidget(self.plot_selector_label)
        left_layout.addWidget(self.plot_selector_combo)

        # Matplotlib figure and canvas
        matplotlib.pyplot.style.use('dark_background')
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        left_layout.addWidget(self.canvas)

        # Add a button to open the InverseTransform window

        self.left_widget = QWidget()  # Crear un widget para contener el layout izquierdo
        self.left_widget.setLayout(left_layout)
        self.left_widget.setMaximumWidth(400)

        # Right side layout - Table
        right_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Adjust the number of columns in the table
        self.table.setHorizontalHeaderLabels(["i", "Xi", "F-1(Xi)"])

        # Add widgets to right layout
        right_layout.addWidget(self.table)

        # Add layouts to main layout
        main_layout.addWidget(self.left_widget)
        main_layout.addLayout(right_layout)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        # endregion

        # region Styles
        self.setStyleSheet("""
                    QWidget {
                        background-color: #333;
                        color: #EEE;
                        font-size: 10pt;
                        font-family: Arial, sans-serif;
                    }
                    QLabel {
                        color: #CCC;
                    }
                    QLineEdit, QComboBox, QTableWidget {
                        background-color: #555;
                        color: #EEE;
                        border: 1px solid #777;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton {
                        background-color: #666;
                        color: #EEE;
                        border: 2px solid #555;
                        border-radius: 5px;
                        padding: 5px;
                        min-height: 15px;
                    }
                    QPushButton:hover {
                        background-color: #777;
                    }
                    QPushButton:pressed {
                        background-color: #888;
                    }
                    QPushButton:disabled {
                        background-color: #444;
                        color: #888;
                    }
                """)
        self.table.setStyleSheet("""
                    QHeaderView::section {
                        background-color: #444;
                        padding: 4px;
                        border: 1px solid #555;
                        font-size: 10pt;
                    }
                    QTableWidget {
                        gridline-color: #666;
                    }
                    QTableWidget::item {
                        border-color: #666;
                    }
                    QScrollBar:horizontal, QScrollBar:vertical {
                        border: 1px solid #666;
                        background: #555;
                        border-radius: 5px;
                    }
                """)
        self.selector_combo.setStyleSheet("""
                    QComboBox::drop-down {
                        border: 0px;
                    }
                    QComboBox::down-arrow {
                        image: url(img/down_arrow.png);
                        width: 14px;
                        height: 14px;
                    }
                """)
        self.plot_selector_combo.setStyleSheet("""
                            QComboBox::drop-down {
                                border: 0px;
                            }
                            QComboBox::down-arrow {
                                image: url(img/down_arrow.png);
                                width: 14px;
                                height: 14px;
                            }
                        """)
        self.generate_button.setStyleSheet("""
                    QPushButton {
                        background-color: #5A5A5A;
                        color: #FFF;
                        border: 1px solid #707070;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #777; /* Color de fondo al pasar el mouse */
                        border: 2px solid #666; /* Color del borde al pasar el mouse */
                    }
                    QPushButton:pressed {
                        background-color: #888; /* Color de fondo al hacer click */
                    }
                """)

        # endregion

        # region Connections
        # Connect the plot selector to the update_plot method
        self.plot_selector_combo.currentIndexChanged.connect(self.update_plot)

        # Connect selector to the method on_change to hide or show the parameters
        self.selector_combo.currentIndexChanged.connect(self.selector_combo_on_change)
        self.selector_combo_on_change()

        # Connect the button to the generate method
        self.generate_button.clicked.connect(self.generate)
        # endregion

        # region Window settings
        # Set the window size
        self.setMaximumSize(1024, 768)
        self.setMinimumSize(600, 450)
        # Set the windows size
        self.resize(750, 550)
        # Set the window icon
        icon = QIcon()
        icon.addFile('img/random.ico')
        self.setWindowIcon(icon)
        # endregion

        # region Validation
        # Set restrictions to the input fields
        self.a_input.setValidator(QDoubleValidator(0.01, 999999999, 2, self))
        self.b_input.setValidator(QDoubleValidator(0.01, 999999999, 2, self))
        # endregion


    def selector_combo_on_change(self):
        # Get the selected method
        method = self.selector_combo.currentText()
        if method == "Uniforme":
            self.a_label.setText("Ingrese a")
            self.b_input.setVisible(True)
            self.b_label.setVisible(True)
        elif method == "Exponencial":
            self.a_label.setText("Ingrese lambda")
            self.b_input.setVisible(False)
            self.b_label.setVisible(False)

    def update_plot(self):
        # Get the selected plot
        plot = self.plot_selector_combo.currentText()

        # Clear the current figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#333333")
        ax.tick_params(colors='#FFFFFF')

        if plot == "Histograma":
            plot_histogram(self.transformed_data, ax, key='F-1(Xi)')
        elif plot == "Dispersión":
            plot_scatter(self.transformed_data, ax, key='F-1(Xi)')
        self.canvas.draw()

    def generate(self):
        # Get the selected method
        method = self.selector_combo.currentText()

        # Get the parameters
        try:
            a = int(self.a_input.text())
            b = int(self.b_input.text()) if self.b_input.isVisible() else None

            # Transform the data
            if method == "Uniforme":
                self.transformed_data = self.__InverseTransform.uniform(a, b)
            elif method == "Exponencial":
                self.transformed_data = self.__InverseTransform.exponential(a)

            # Update the table
            self.table.setRowCount(0)
            for row in self.transformed_data:
                self.table.insertRow(self.table.rowCount())
                for i, key in enumerate(row.keys()):
                    self.table.setItem(self.table.rowCount() - 1, i, QTableWidgetItem(str(row[key])))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return


        # Update the plot
        self.update_plot()
        self.table.resizeColumnsToContents()

    def closeEvent(self, event):
        self.close_window.emit()
        super().closeEvent(event)
