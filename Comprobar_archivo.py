import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random

class FolderCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Update Checker")
        
        # Establecer la ventana
        self.root.geometry("500x500")
        
        # Crear la lista de carpetas seleccionadas
        self.folder_list = []
        
        # Variable de control para el bucle
        self.running = False
        self.checking_thread = None

        # Crear los elementos de la GUI
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta de instrucciones
        instructions = ttk.Label(self.root, text="Selecciona carpetas para verificar si están actualizadas:")
        instructions.pack(pady=10)

        # Marco para los botones de selección
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        # Botón para seleccionar carpetas
        select_button = ttk.Button(button_frame, text="Agregar Carpeta", command=self.select_folders)
        select_button.pack(side=tk.LEFT, padx=5)

        # Botón para eliminar carpetas
        self.remove_button = ttk.Button(button_frame, text="Eliminar Carpeta", command=self.remove_folders, state=tk.DISABLED)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        # Lista de carpetas seleccionadas
        self.folder_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=10)
        self.folder_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Entrada para el intervalo de tiempo
        interval_label = ttk.Label(self.root, text="Intervalo de tiempo para comprobar (en minutos):")
        interval_label.pack(pady=10)
        self.interval_entry = ttk.Entry(self.root)
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, "1")  # Valor predeterminado de 1 minuto

        # Marco para los botones de control
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        # Botón para iniciar la verificación continua
        start_button = ttk.Button(control_frame, text="Iniciar Verificación", command=self.start_checking)
        start_button.pack(side=tk.LEFT, padx=5)

        # Botón para detener la verificación continua
        stop_button = ttk.Button(control_frame, text="Detener", command=self.stop_checking)
        stop_button.pack(side=tk.LEFT, padx=5)

        # Botón para salir de la aplicación
        exit_button = ttk.Button(control_frame, text="Salir", command=self.exit_program)
        exit_button.pack(side=tk.LEFT, padx=5)

        # Indicador de estado mejorado
        status_frame = ttk.Frame(self.root)
        status_frame.pack(pady=10, fill=tk.X)
        status_label = ttk.Label(status_frame, text="Estado:", font=("Arial", 10, "bold"))
        status_label.pack(side=tk.LEFT)

        self.status_indicator = tk.Canvas(status_frame, width=20, height=20, bg="red", highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, padx=5)

        # Mejora del estilo del indicador
        self.status_indicator.create_oval(2, 2, 18, 18, fill="red", outline="")

    def select_folders(self):
        folders = filedialog.askdirectory(mustexist=True)
        if folders:
            self.folder_list.append(folders)
            self.folder_listbox.insert(tk.END, folders)

    def remove_folders(self):
        selected_indices = self.folder_listbox.curselection()
        for index in reversed(selected_indices):
            self.folder_listbox.delete(index)
            del self.folder_list[index]  # Eliminar de la lista de carpetas

    def start_checking(self):
        if not self.folder_list:
            messagebox.showwarning("Advertencia", "Por favor, selecciona al menos una carpeta.")
            return
        
        try:
            interval = int(self.interval_entry.get()) * 60  # Convertir minutos a segundos
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor numérico válido para el intervalo.")
            return
        
        self.running = True
        self.update_indicator()  # Iniciar el parpadeo del indicador
        self.remove_button.config(state=tk.DISABLED)  # Deshabilitar el botón al iniciar la verificación

        # Crear un hilo daemon para la verificación
        self.checking_thread = threading.Thread(target=self.check_folders_periodically, args=(interval,), daemon=True)
        self.checking_thread.start()

    def stop_checking(self):
        self.running = False
        self.status_indicator.config(bg="red")  # Cambiar el indicador a rojo
        self.remove_button.config(state=tk.NORMAL)  # Habilitar el botón al detener la verificación

    def exit_program(self):
        self.running = False
        self.root.quit()  # Cerrar la ventana de la GUI

    def check_folders_periodically(self, interval):
        while self.running:
            for folder in self.folder_list:
                if self.check_folder_update(folder):
                    messagebox.showinfo("Notificación", f"La carpeta '{folder}' no se ha actualizado en los últimos 15 minutos.")
            time.sleep(interval)

    def check_folder_update(self, folder_path, time_limit_minutes=15):
        try:
            folder_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(folder_path))
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener la fecha de modificación de {folder_path}: {e}")
            return False
        
        current_time = datetime.datetime.now()
        time_difference = current_time - folder_mod_time
        
        if time_difference.total_seconds() > time_limit_minutes * 60:
            return True  # Desactualizada
        else:
            return False  # Actualizada

    def update_indicator(self):
        if self.running:
            # Parpadeo errático
            new_color = random.choice(["green", "light green", "dark green"])
            self.status_indicator.itemconfig(1, fill=new_color)  # Cambia el color del óvalo
            delay = random.randint(100, 500)  # Delay aleatorio entre 100ms y 500ms
            self.root.after(delay, self.update_indicator)
        else:
            self.status_indicator.itemconfig(1, fill="red")  # Cambiar a rojo si se detiene

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderCheckerApp(root)
    root.mainloop()
