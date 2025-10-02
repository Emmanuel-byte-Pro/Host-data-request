import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from sftp_client import sftp_transfer
import threading

class SftpUploaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SFTP Image Uploader")
        self.geometry("600x500")
        self.create_widgets()

    def create_widgets(self):
        # Frame para las credenciales y la información del servidor
        connection_frame = ttk.LabelFrame(self, text="Datos de Conexión", padding=(10, 5))
        connection_frame.pack(padx=10, pady=5, fill="x")

        # --- Widgets de conexión ---
        ttk.Label(connection_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.host_entry = ttk.Entry(connection_frame, width=40)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(connection_frame, text="Puerto:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.port_entry.insert(0, "22")

        ttk.Label(connection_frame, text="Usuario:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.user_entry = ttk.Entry(connection_frame, width=40)
        self.user_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(connection_frame, text="Contraseña:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(connection_frame, show="*", width=40)
        self.password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Frame para los directorios
        dir_frame = ttk.LabelFrame(self, text="Directorios", padding=(10, 5))
        dir_frame.pack(padx=10, pady=5, fill="x")

        # --- Widgets de directorios ---
        ttk.Label(dir_frame, text="Directorio Remoto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.remote_dir_entry = ttk.Entry(dir_frame, width=40)
        self.remote_dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.select_dir_button = ttk.Button(dir_frame, text="Seleccionar Carpeta Local", command=self.select_local_directory)
        self.select_dir_button.grid(row=1, column=0, padx=5, pady=10)

        self.local_dir_label = ttk.Label(dir_frame, text="Ninguna carpeta seleccionada", foreground="gray")
        self.local_dir_label.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        self.local_dir_path = ""

        # Botón para iniciar la transferencia
        self.upload_button = ttk.Button(self, text="Iniciar Transferencia", command=self.start_upload_thread)
        self.upload_button.pack(pady=10)

        # Área de texto para el estado/log
        self.status_log = scrolledtext.ScrolledText(self, height=10, state="disabled")
        self.status_log.pack(padx=10, pady=10, fill="both", expand=True)

    def select_local_directory(self):
        """Abre un diálogo para seleccionar el directorio local."""
        path = filedialog.askdirectory(title="Seleccionar Carpeta de Imágenes")
        if path:
            self.local_dir_path = path
            self.local_dir_label.config(text=path, foreground="black")

    def log_status(self, message):
        """Añade un mensaje al área de log de la GUI."""
        self.status_log.config(state="normal")
        self.status_log.insert(tk.END, message + "\n")
        self.status_log.config(state="disabled")
        self.status_log.see(tk.END)

    def start_upload_thread(self):
        """Inicia la transferencia en un hilo separado para no bloquear la GUI."""
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        user = self.user_entry.get()
        password = self.password_entry.get()
        remote_dir = self.remote_dir_entry.get()

        if not all([host, port, user, password, self.local_dir_path, remote_dir]):
            self.log_status("Error: Todos los campos son obligatorios.")
            return

        self.upload_button.config(state="disabled")
        self.log_status("--- Iniciando transferencia ---")

        transfer_thread = threading.Thread(
            target=sftp_transfer,
            args=(host, port, user, password, self.local_dir_path, remote_dir, self.log_status_threadsafe)
        )
        transfer_thread.daemon = True
        transfer_thread.start()

    def log_status_threadsafe(self, message):
        """Función segura para hilos para actualizar el log."""
        self.after(0, self.log_status, message)
        if "Transferencia de archivos completada" in message or "Error" in message:
            self.after(0, lambda: self.upload_button.config(state="normal"))

if __name__ == "__main__":
    app = SftpUploaderApp()
    app.mainloop()