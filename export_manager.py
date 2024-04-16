class ExportManager:
    def __init__(self, glossary_manager):
        """Inicializa el ExportManager con una instancia de GlossaryManager."""
        self.glossary_manager = glossary_manager

    def export_to_latex(self, author: str, title: str, file_path: str) -> None:
        """Exporta el glosario a un documento LaTeX y lo guarda en un archivo."""
        latex_document = self.glossary_manager.to_latex(author, title)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(latex_document)

    def export_to_md(self, author: str, title: str, file_path: str) -> None:
        """Exporta el glosario a un documento Markdown y lo guarda en un archivo."""
        md_document = self.glossary_manager.to_md(author, title)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(md_document)

    def export_to_html(self, author: str, title: str, file_path: str) -> None:
        """Exporta el glosario a un documento HTML y lo guarda en un archivo."""
        html_document = self.glossary_manager.to_html(author, title)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_document)

    def export_to_docx(self, author: str, title: str, file_path: str) -> None:
        """Exporta el glosario a un documento Word (docx) y lo guarda en un archivo."""
        docx_filename = self.glossary_manager.to_docx(author, title, file_path)
        # Si se desea, se puede imprimir un mensaje confirmando la exportación
        print(f"Documento Word (docx) guardado en {docx_filename}.")

    def export_to_xml(self, author: str, title: str, file_path: str) -> None:
        """Exporta el glosario a un documento XML y lo guarda en un archivo."""
        xml_document = self.glossary_manager.to_xml(author, title)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(xml_document)
