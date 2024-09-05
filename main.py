import argparse

from process_csv.process_columns import process_csv
from UI_module.DragADrop import DragDropApp


def scan_directory(directory_path):
    # Implementa la lógica para escanear el directorio
    print(f"Escaneando el directorio: {directory_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Aplicación Drag and Drop para archivos CSV",
        add_help=True,
    )
    # Crear un grupo de argumentos mutuamente excluyentes
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-f", "--file", type=str, help="Ruta al archivo CSV")
    group.add_argument(
        "-d", "--directory", type=str, help="Ruta al directorio a escanear"
    )
    args = parser.parse_args()

    if args.file:
        if args.file.endswith(".csv"):
            process_csv(args.file)
        else:
            print("Por favor, proporciona un archivo CSV válido.")
    elif args.directory:
        scan_directory(args.directory)
    else:
        print("Se procede a iniciar la Interfáz gráfica.")

        app = DragDropApp()
        app.mainloop()


if __name__ == "__main__":
    main()

    # extra code – code to save the figures as high-res PNGs for the book
    # main()


# extra code – code to save the figures as high-res PNGs for the book
