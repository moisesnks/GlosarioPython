class ExportManager:
    def __init__(self, glossary_manager):
        """Inicializa el ExportManager con una instancia de GlossaryManager."""
        self.glossary_manager = glossary_manager

    def export_to_latex(self, author: str, title: str, file_path: str) -> tuple[bool, str]:
        """Exporta el glosario a un documento LaTeX y lo guarda en un archivo."""
        try:
            latex_document = self.glossary_manager.to_latex(author, title)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(latex_document)
            return True, f"El glosario se ha exportado correctamente a LaTeX en '{file_path}'."
        except Exception as e:
            return False, f"Error al exportar a LaTeX: {str(e)}"

    def export_to_md(self, author: str, title: str, file_path: str) -> tuple[bool, str]:
        """Exporta el glosario a un documento Markdown y lo guarda en un archivo."""
        try:
            md_document = self.glossary_manager.to_md(author, title)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(md_document)
            return True, f"El glosario se ha exportado correctamente a Markdown en '{file_path}'."
        except Exception as e:
            return False, f"Error al exportar a Markdown: {str(e)}"

    def export_to_html(self, author: str, title: str, file_path: str) -> tuple[bool, str]:
        """Exporta el glosario a un documento HTML y lo guarda en un archivo."""
        try:
            html_document = self.glossary_manager.to_html(author, title)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_document)
            return True, f"El glosario se ha exportado correctamente a HTML en '{file_path}'."
        except Exception as e:
            return False, f"Error al exportar a HTML: {str(e)}"

    def export_to_docx(self, author: str, title: str, file_path: str) -> tuple[bool, str]:
        """Exporta el glosario a un documento Word (docx) y lo guarda en un archivo."""
        try:
            docx_filename = self.glossary_manager.to_docx(author, title, file_path)
            return True, f"El glosario se ha exportado correctamente a DOCX en '{file_path}'."
        except Exception as e:
            return False, f"Error al exportar a DOCX: {str(e)}"

    def export_to_xml(self, author: str, title: str, file_path: str) -> tuple[bool, str]:
        """Exporta el glosario a un documento XML y lo guarda en un archivo."""
        try:
            xml_document = self.glossary_manager.to_xml(author, title)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(xml_document)
            return True, f"El glosario se ha exportado correctamente a XML en '{file_path}'."
        except Exception as e:
            return False, f"Error al exportar a XML: {str(e)}"
