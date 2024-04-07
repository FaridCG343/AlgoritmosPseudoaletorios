import matplotlib.pyplot
from PySide6.QtGui import QIntValidator, QIcon
from PySide6.QtWidgets import (QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QGridLayout,
                               QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.PseudoRandom import PseudoRandom
from views.InverseTransformVw import InverseTransformVw
from utils.Plots import plot_scatter, plot_box, plot_variance


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.inverse_transform = None
        self.list_generated = []

        # region Main layout
        # Main layout
        main_layout = QHBoxLayout()

        # Left side layout
        input_layout = QGridLayout()

        # Selector with methods from PseudoRandom class
        self.selector_label = QLabel("Selector")
        self.selector_combo = QComboBox()
        self.selector_combo.addItems(["Cuadrados Medios", "Congruencial Lineal", "Congruencial Cuadratico"])
        input_layout.addWidget(self.selector_label, 0, 0)
        input_layout.addWidget(self.selector_combo, 0, 1)

        # Seed and parameters input
        self.seed_label = QLabel("Ingrese la semilla")
        self.seed_input = QLineEdit()
        self.a_label = QLabel("Ingrese a")
        self.a_input = QLineEdit()
        self.b_label = QLabel("Ingrese b")
        self.b_input = QLineEdit()
        self.c_label = QLabel("Ingrese c")
        self.c_input = QLineEdit()
        self.m_label = QLabel("Ingrese m")
        self.m_input = QLineEdit()

        # Add widgets to left layout
        input_layout.addWidget(self.seed_label, 1, 0)
        input_layout.addWidget(self.seed_input, 1, 1)
        input_layout.addWidget(self.a_label, 2, 0)
        input_layout.addWidget(self.a_input, 2, 1)
        input_layout.addWidget(self.b_label, 3, 0)
        input_layout.addWidget(self.b_input, 3, 1)
        input_layout.addWidget(self.c_label, 4, 0)
        input_layout.addWidget(self.c_input, 4, 1)
        input_layout.addWidget(self.m_label, 5, 0)
        input_layout.addWidget(self.m_input, 5, 1)

        # Generate button
        self.generate_button = QPushButton("Generar")
        input_layout.addWidget(self.generate_button, 6, 0, 1, 2)

        # Left side layout
        left_layout = QVBoxLayout()
        left_layout.addLayout(input_layout)
        left_layout.addStretch()  # This will push the grid layout to the top


        self.plot_selector_label = QLabel("Seleccione el tipo de gráfico:")
        self.plot_selector_combo = QComboBox()
        self.plot_selector_combo.addItems(["Dispersión", "Box Plot", "Varianza"])
        left_layout.addWidget(self.plot_selector_label)
        left_layout.addWidget(self.plot_selector_combo)

        # Matplotlib figure and canvas
        matplotlib.pyplot.style.use('dark_background')
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        left_layout.addWidget(self.canvas)

        # Add a button to open the InverseTransform window
        self.inverse_transform_button = QPushButton("Transformada Inversa")
        self.inverse_transform_button.setEnabled(False)
        left_layout.addWidget(self.inverse_transform_button)

        self.left_widget = QWidget()  # Crear un widget para contener el layout izquierdo
        self.left_widget.setLayout(left_layout)
        self.left_widget.setMaximumWidth(400)

        # Right side layout - Table
        right_layout = QVBoxLayout()
        self.quantity_label = QLabel("Cantidad de numeros a generar")
        self.quantity_input = QLineEdit()
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Adjust the number of columns in the table
        self.table.setHorizontalHeaderLabels(["i", "left", "xi", "right", "ri"])

        # Add widgets to right layout
        right_layout.addWidget(self.quantity_label)
        right_layout.addWidget(self.quantity_input)
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

        # Connect the button to the display_inverse_transform method
        self.inverse_transform_button.clicked.connect(self.display_inverse_transform)
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
        self.seed_input.setValidator(QIntValidator(1, 999999999, self))
        self.quantity_input.setValidator(QIntValidator(1, 999999999, self))
        self.a_input.setValidator(QIntValidator(1, 999999999, self))
        self.b_input.setValidator(QIntValidator(1, 999999999, self))
        self.c_input.setValidator(QIntValidator(1, 999999999, self))
        self.m_input.setValidator(QIntValidator(1, 999999999, self))
        # endregion

    def selector_combo_on_change(self):
        # Get the selected method
        method = self.selector_combo.currentText()
        self.a_label.setVisible(method != "Cuadrados Medios")
        self.a_input.setVisible(method != "Cuadrados Medios")
        self.b_label.setVisible(method == "Congruencial Cuadratico")
        self.b_input.setVisible(method == "Congruencial Cuadratico")
        self.c_label.setVisible(method != "Cuadrados Medios")
        self.c_input.setVisible(method != "Cuadrados Medios")
        self.m_label.setVisible(method != "Cuadrados Medios")
        self.m_input.setVisible(method != "Cuadrados Medios")

    def update_plot(self):
        # Get the selected plot type
        plot_type = self.plot_selector_combo.currentText()

        # Clear the current figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#333333")
        ax.tick_params(colors='#FFFFFF')

        # Get the data
        data = self.list_generated

        # Depending on the selection, update the plot
        if plot_type == "Dispersión":
            plot_scatter(data, ax)
        elif plot_type == "Corrida arriba/abajo":
            # plot_run_sequence(data, ax)
            pass
        elif plot_type == "Box Plot":
            plot_box(data, ax)
        elif plot_type == "Varianza":
            plot_variance(data, ax)

        # Redraw the canvas
        self.canvas.draw()

    def generate(self):
        # Get the selected method
        method = self.selector_combo.currentText()
        try:
            # Get the seed
            seed = int(self.seed_input.text())
            # Get the quantity
            quantity = int(self.quantity_input.text())
        except ValueError:
            # display an error message
            QMessageBox.critical(self, "Error", "La semilla y la cantidad deben ser números enteros positivos.")
            return
        pseudo_random = PseudoRandom(seed)

        try:
            if method == "Cuadrados Medios":
                # Get the generated list
                list_generated = pseudo_random.middle_square(quantity)
            else:
                # Get the parameters
                a = int(self.a_input.text() if self.a_input.text() else 0)
                c = int(self.c_input.text() if self.c_input.text() else 0)
                m = int(self.m_input.text() if self.m_input.text() else 0)
                if method == "Congruencial Lineal":
                    # Get the generated list
                    list_generated = pseudo_random.linear_congruential(quantity, a, c, m)
                else:
                    b = int(self.b_input.text() if self.b_input.text() else 0)
                    # Get the generated list
                    list_generated = pseudo_random.quadratic_congruential(quantity, a, b, c, m)
        except Exception as e:
            # Display an error message
            QMessageBox.critical(self, "Error", str(e))
            return

        # if the len of the list is less than the quantity, display an info message
        if len(list_generated) < quantity:
            QMessageBox.information(self, "Información", "La secuencia se repitió, se generaron " +
                                    str(len(list_generated)) + " números.")
        # Clear the table
        self.table.clearContents()
        self.table.setRowCount(0)

        # Set headers based on the first element of the list
        self.table.setColumnCount(len(list_generated[0].keys()))
        self.table.setHorizontalHeaderLabels(list(list_generated[0].keys()))
        # Add the generated list to the table
        for row_number, row_data in enumerate(list_generated):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data.values()):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Plot the data
        self.list_generated = list_generated
        self.update_plot()

        # Resize the columns to fit the content
        self.table.resizeColumnsToContents()

        # Enable the inverse transform button
        self.inverse_transform_button.setEnabled(True)

    def display_inverse_transform(self):
        data = [float(dic['ri']) for dic in self.list_generated if 'ri' in dic]
        self.inverse_transform = InverseTransformVw(data)
        self.inverse_transform.close_window.connect(self.show)
        self.inverse_transform.show()
        self.hide()
