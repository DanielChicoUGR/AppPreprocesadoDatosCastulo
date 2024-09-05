import tkinter as tk
from pathlib import Path
from tkinter import Canvas, filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD

from process_csv.process_columns import process_csv

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"/home/daniel/Proyectos/ScriptsCastulo/UI_module/assets/"
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class DragDropApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drag and Drop CSV Viewer")
        self.geometry("1440x1024")
        self.configure(bg="#15D734")

        # Variable para el modo de procesado
        self.process_mode = tk.StringVar(value="file")

        # Crear los widgets
        self.create_widgets()

    def create_widgets(self):
        canvas = Canvas(
            self,
            bg="#15D734",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=0, y=0)
        canvas.create_rectangle(1.0, 0.0, 544.0, 1024.0, fill="#93E8A1", outline="")

        canvas.create_text(
            35.0,
            156.0,
            anchor="nw",
            text="Generación de un CSV listo para trabajar en el\nanálisis de datos",
            fill="#000000",
            font=("Inter", 15 * -1),
            justify="center"
        )

        canvas.create_text(
            35.0,
            54.0,
            anchor="nw",
            text="Procesado de Datos CSV. ",
            fill="#000000",
            font=("Inter", 36 * -1)
        )

        canvas.create_rectangle(
            -1.0,
            233.0,
            543.0000092967966,
            234.99999999686486,
            fill="#3E2E6B",
            outline="",
        )

        # button_image_1 = PhotoImage(
        #     file=relative_to_assets("button_1.png"))
        # button_1 = Button(
        #     image=button_image_1,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: print("button_1 clicked"),
        #     relief="flat"
        # )
        # button_1.place(
        #     x=105.0,
        #     y=500.0,
        #     width=333.0,
        #     height=83.0
        # )

        # button_image_2 = PhotoImage(
        #     file=relative_to_assets("button_2.png"))
        # button_2 = Button(
        #     image=button_image_2,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: print("button_2 clicked"),
        #     relief="flat"
        # )
        # button_2.place(
        #     x=105.0,
        #     y=333.0,
        #     width=333.0,
        #     height=83.0
        # )

        # Frame para los radiobuttons
        frame_options = tk.Frame(self, bg="#93E8A1")
        frame_options.place(x=35, y=250)

        # Radiobutton para seleccionar el modo de procesado
        tk.Radiobutton(
            frame_options,
            text="Archivo único",
            variable=self.process_mode,
            value="file",
            bg="#93E8A1",
            font=("Arial", 12),
        ).pack(anchor="w", pady=5)
        tk.Radiobutton(
            frame_options,
            text="Carpeta",
            variable=self.process_mode,
            value="directory",
            bg="#93E8A1",
            font=("Arial", 12),
        ).pack(anchor="w", pady=5)

        # Frame para la zona de arrastrar y soltar
        frame_drop = tk.Frame(self, bg="#ffffff", relief="solid", bd=1)
        frame_drop.place(x=600, y=200)

        self.label = tk.Label(
            frame_drop,
            text="Arrastra y suelta un archivo CSV aquí",
            width=40,
            height=10,
            bg="#ffffff",
            font=("Arial", 12),
            relief="solid",
            bd=1,
        )
        self.label.pack(padx=10, pady=10)

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drop)

        # Bind para abrir el diálogo de selección al hacer clic en la etiqueta
        self.label.bind("<Button-1>", self.open_file_dialog)

    def drop(self, event):
        file_path = event.data
        print(f"Archivo CSV seleccionado: {file_path}")
        if file_path.endswith(".csv"):
            process_csv(file_path)
            self.destroy()
        else:
            print("Por favor, arrastra un archivo CSV.")

    def open_file_dialog(self, event):
        if self.process_mode.get() == "file":
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                print(f"Archivo CSV seleccionado: {file_path}")
                if file_path.endswith(".csv"):
                    process_csv(file_path)
                    self.destroy()
                else:
                    messagebox.showerror(
                        "Error", "Por favor, selecciona un archivo CSV válido."
                    )
        elif self.process_mode.get() == "directory":
            directory_path = filedialog.askdirectory()
            if directory_path:
                print(f"Directorio seleccionado: {directory_path}")
                # Aquí puedes llamar a una función para procesar el directorio
                # process_directory(directory_path)
                self.destroy()
