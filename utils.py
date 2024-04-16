def generate_css(path: str) -> None:
    """Generar un archivo CSS para el html generado."""
    with open(path, "w") as file:
        file.write("body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; background-color: #f9f9f9; max-width: 800px; margin: auto; } h1, h2 { color: #333; } h1 { font-size: 2rem; margin-bottom: 10px; } h2 { font-size: 1.5rem; margin-top: 20px; margin-bottom: 10px; border-bottom: 2px solid #333; padding-bottom: 5px; } p { margin-bottom: 10px; } ul { margin-left: 20px; margin-bottom: 10px; } ul li { margin-bottom: 5px; } strong { color: #555; }")
    print(f"Archivo CSS generado en '{path}'.")

if __name__ == "__main__":
    generate_css("output/styles.css")