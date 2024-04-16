import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, QAction, QLabel, QPushButton, QTextBrowser, QListWidget, QListWidgetItem, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt

import glosario_manager
from export_manager import ExportManager

class GlossaryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configura el título y tamaño de la ventana
        self.setWindowTitle("Glosario de Términos Ágiles")
        self.setGeometry(100, 100, 800, 600)

        # Cargar glosario desde el archivo XML
        self.glossary_manager = glosario_manager.GlossaryManager()
        self.glossary_manager.load_glossary("input/glosario_agil.xml")

        # Crear una instancia de ExportManager
        self.export_manager = ExportManager(self.glossary_manager)

        # Configura el menú
        self.setup_menu()

        # Variables para controlar la navegación
        self.term_list_items = list(self.glossary_manager.glosario.keys())

        # Configura el contenedor central
        self.setup_central_widget()

        # Muestra el primer término de la lista
        self.show_selected_term()

        # Inicializa el índice actual
        self.current_index = 0

        # Conectar las señales de los campos de edición a la función de actualización
        self.term_edit.textChanged.connect(self.update_preview)
        self.definition_edit.textChanged.connect(self.update_preview)
        self.examples_edit.textChanged.connect(self.update_preview)

    def setup_menu(self):
        """Configura la barra de menú."""
        menu_bar = self.menuBar()
        export_menu = menu_bar.addMenu("Exportar")

        # Crear acciones del menú
        export_to_latex = QAction("Exportar a LaTeX", self)
        export_to_md = QAction("Exportar a Markdown", self)
        export_to_html = QAction("Exportar a HTML", self)
        export_to_docx = QAction("Exportar a Word", self)

        # Conectar acciones con funciones del ExportManager
        export_to_latex.triggered.connect(lambda: self.export_manager.export_to_latex("Autor", "Título", "output/glosario_agil.tex"))
        export_to_md.triggered.connect(lambda: self.export_manager.export_to_md("Autor", "Título", "output/glosario_agil.md"))
        export_to_html.triggered.connect(lambda: self.export_manager.export_to_html("Autor", "Título", "output/glosario_agil.html"))
        export_to_docx.triggered.connect(lambda: self.export_manager.export_to_docx("Autor", "Título", "output/glosario_agil.docx"))

        # Agregar acciones al menú
        export_menu.addAction(export_to_latex)
        export_menu.addAction(export_to_md)
        export_menu.addAction(export_to_html)
        export_menu.addAction(export_to_docx)

    def setup_central_widget(self):
        """Configura el contenedor central de la aplicación."""
        # Crear el contenedor central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Configura un diseño horizontal para las páginas
        h_layout = QHBoxLayout(central_widget)

        # Configura el lado izquierdo (página izquierda)
        left_page = self.setup_left_page()
        h_layout.addWidget(left_page)

        # Configura el lado derecho (página derecha)
        right_page = self.setup_right_page()
        h_layout.addWidget(right_page)

    def setup_left_page(self):
        """Configura la página izquierda con sus elementos."""
        # Crear un contenedor para la página izquierda
        left_page = QWidget()
        layout = QVBoxLayout(left_page)

        # Crear un widget para mostrar la lista de términos
        self.term_list = QListWidget()
        self.term_list.addItems(self.term_list_items)
        self.term_list.itemSelectionChanged.connect(self.show_selected_term)
        layout.addWidget(self.term_list)

        # Crear widgets para editar término y definición
        self.term_edit = QLineEdit()
        layout.addWidget(QLabel("Término:"))
        layout.addWidget(self.term_edit)

        self.definition_edit = QTextEdit()
        layout.addWidget(QLabel("Definición:"))
        layout.addWidget(self.definition_edit)

        self.examples_edit = QTextEdit()
        layout.addWidget(QLabel("Ejemplos:"))
        layout.addWidget(self.examples_edit)

        # Crear botones para guardar, nuevo, añadir y borrar
        buttons_layout = QVBoxLayout()

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_term)
        buttons_layout.addWidget(save_button)

        new_button = QPushButton("Nuevo")
        new_button.clicked.connect(self.blank_term)
        buttons_layout.addWidget(new_button)

        add_button = QPushButton("Añadir")
        add_button.clicked.connect(self.add_term)
        buttons_layout.addWidget(add_button)

        delete_button = QPushButton("Borrar")
        delete_button.clicked.connect(self.delete_term)
        buttons_layout.addWidget(delete_button)

        # Crear botones de navegación en fila
        nav_layout = QHBoxLayout()  # Cambiar a fila
        prev_button = QPushButton("←")
        prev_button.clicked.connect(self.prev_term)
        nav_layout.addWidget(prev_button)

        next_button = QPushButton("→")
        next_button.clicked.connect(self.next_term)
        nav_layout.addWidget(next_button)

        # Agregar botones de orden
        sort_asc_button = QPushButton("Ordenar A-Z")
        sort_asc_button.clicked.connect(self.sort_terms_asc)
        buttons_layout.addWidget(sort_asc_button)

        sort_desc_button = QPushButton("Ordenar Z-A")
        sort_desc_button.clicked.connect(self.sort_terms_desc)
        buttons_layout.addWidget(sort_desc_button)

        # Agregar botones al diseño principal de la página izquierda
        layout.addLayout(buttons_layout)

        return left_page

    def setup_right_page(self):
        """Configura la página derecha con su área de texto para previsualizar."""
        # Crear un contenedor para la página derecha
        right_page = QWidget()
        layout = QVBoxLayout(right_page)

        # Crear un área de texto para mostrar el término y su definición
        self.text_browser = QTextBrowser()
        layout.addWidget(self.text_browser)

        return right_page

    def show_selected_term(self):
        """Mostrar el término seleccionado en la lista."""
        selected_items = self.term_list.selectedItems()
        if selected_items:
            self.current_term = selected_items[0].text()
            self.current_index = self.term_list_items.index(self.current_term)
            self.show_term_info()
        else:
            self.current_term = None

    def show_term_info(self):
        """Mostrar la información del término actual."""
        if self.current_term is None:
            return

        term_data = self.glossary_manager.get_term(self.current_term)
        if term_data:
            self.term_edit.setText(self.current_term)
            self.definition_edit.setText(term_data.get("definicion", ""))
            examples_text = '\n'.join(term_data.get("ejemplos", []))
            self.examples_edit.setText(examples_text)

            # Mostrar el contenido en el área de texto de previsualización
            content = f"<h2>{self.current_term}</h2><p><strong>Definición:</strong> {term_data.get('definicion', '')}</p><p><strong>Ejemplos:</strong></p><ul>"
            for ejemplo in term_data.get("ejemplos", []):
                content += f"<li>{ejemplo}</li>"
            content += "</ul>"
            self.text_browser.setHtml(content)

    def update_preview(self):
        """Actualiza la previsualización en self.text_browser basado en los campos de edición."""
        # Obtener el contenido de los campos de edición
        term_name = self.term_edit.text().strip()
        term_definition = self.definition_edit.toPlainText().strip()
        examples_text = self.examples_edit.toPlainText().strip()

        # Crear contenido HTML para la previsualización
        content = f"<h2>{term_name}</h2><p><strong>Definición:</strong> {term_definition}</p><p><strong>Ejemplos:</strong></p><ul>"
        for example in examples_text.split('\n'):
            content += f"<li>{example}</li>"
        content += "</ul>"

        # Establecer el contenido en el QTextBrowser
        self.text_browser.setHtml(content)

    # Función para dejar en blanco los campos de edición
    def blank_term(self):
        """Manejar el proceso de agregar un nuevo término."""
        # Limpia los campos de entrada para que el usuario pueda ingresar un nuevo término
        self.term_edit.clear()
        self.definition_edit.clear()
        self.examples_edit.clear()

    def add_term(self):
        """Agregar un nuevo término al glosario."""
        term_name = self.term_edit.text().strip()
        term_definition = self.definition_edit.toPlainText().strip()
        examples = self.examples_edit.toPlainText().strip().split('\n')

        # Validar que el nombre del término no esté vacío
        if not term_name:
            QMessageBox.warning(self, "Error", "El término no puede estar vacío.")
            return

        # Guardar el término usando GlossaryManager
        self.glossary_manager.add_term(term_name, term_definition, examples)

        # Actualizar la lista de términos
        self.term_list.clear()
        self.term_list_items = list(self.glossary_manager.glosario.keys())
        self.term_list.addItems(self.term_list_items)

        # Seleccionar el nuevo término
        items = self.term_list.findItems(term_name, Qt.MatchExactly)
        if items:
            self.term_list.setCurrentItem(items[0])

        # Sobreescribe el XML
        self.glossary_manager.save_glossary("input/glosario_agil.xml")
        QMessageBox.information(self, "Éxito", "El término ha sido añadido.")


    def save_term(self):
        """Guardar el término editado."""
        term_name = self.term_edit.text().strip()
        term_definition = self.definition_edit.toPlainText().strip()
        examples = self.examples_edit.toPlainText().strip().split('\n')

        # Validar que el nombre del término no esté vacío
        if not term_name:
            QMessageBox.warning(self, "Error", "El término no puede estar vacío.")
            return

        # Guardar el término usando GlossaryManager
        self.glossary_manager.save_term(term_name, term_definition, examples)

        # Actualizar la lista de términos
        if self.current_term != term_name:
            self.term_list.clear()
            self.term_list_items = list(self.glossary_manager.glosario.keys())
            self.term_list.addItems(self.term_list_items)
            # Seleccionar el nuevo término
            items = self.term_list.findItems(term_name, Qt.MatchExactly)
            if items:
                self.term_list.setCurrentItem(items[0])

        # Sobreescribe el XML
        self.glossary_manager.save_glossary("input/glosario_agil.xml")
        QMessageBox.information(self, "Éxito", "El término ha sido guardado.")

    def delete_term(self):
        """Borrar el término seleccionado."""
        selected_items = self.term_list.selectedItems()
        if selected_items:
            term_to_delete = selected_items[0].text()
            # Confirmar la acción con un mensaje emergente
            reply = QMessageBox.question(self, "Confirmar Borrado", f"¿Estás seguro de que deseas borrar el término '{term_to_delete}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.glossary_manager.delete_term(term_to_delete)
                self.term_list.takeItem(self.term_list.currentRow())
                self.term_edit.clear()
                self.definition_edit.clear()
                self.examples_edit.clear()
                self.text_browser.clear()
                # Sobreescribe el XML
                self.glossary_manager.save_glossary("input/glosario_agil.xml")
                QMessageBox.information(self, "Éxito", "El término ha sido borrado.")

    def sort_terms_asc(self):
        """Ordenar los términos de forma ascendente."""
        self.term_list_items.sort()
        self.term_list.clear()
        self.term_list.addItems(self.term_list_items)

    def sort_terms_desc(self):
        """Ordenar los términos de forma descendente."""
        self.term_list_items.sort(reverse=True)
        self.term_list.clear()
        self.term_list.addItems(self.term_list_items)

    def prev_term(self):
        """Navegar al término anterior."""
        if self.current_index > 0:
            self.current_index -= 1
            self.current_term = self.term_list_items[self.current_index]
            self.show_term_info()
            # Seleccionar el término en la lista
            self.term_list.setCurrentRow(self.current_index)

    def next_term(self):
        """Navegar al siguiente término."""
        if self.current_index < len(self.term_list_items) - 1:
            self.current_index += 1
            self.current_term = self.term_list_items[self.current_index]
            self.show_term_info()
            # Seleccionar el término en la lista
            self.term_list.setCurrentRow(self.current_index)

# Crear la aplicación
app = QApplication(sys.argv)
glossary_app = GlossaryApp()
glossary_app.show()

# Ejecutar la aplicación
sys.exit(app.exec_())
