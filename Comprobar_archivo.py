import os
import datetime
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import messagebox, filedialog
import threading

folder_paths = []
toaster = ToastNotifier()
checking = False  # Variable global para controlar el estado de la comprobación

def add_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_paths.append(folder_path)
        update_ui()

def remove_folder():
    selected_folder = folder_listbox.curselection()
    if selected_folder:
        folder_paths.pop(selected_folder[0])
        update_ui()

def check_folder():
    global checking
    results = []
    for folder_path in folder_paths:
        if not checking:
            break
        folder_name = os.path.basename(folder_path)
        identifier = folder_name.split("_")[0]

        if os.path.isdir(folder_path):
            mod_time = os.path.getmtime(folder_path)
            mod_time = datetime.datetime.fromtimestamp(mod_time)
            formatted_mod_time = mod_time.strftime("%Y-%m-%d %H:%M")
            current_time = datetime.datetime.now()
            time_difference = (current_time - mod_time).total_seconds() / 60

            if time_difference <= 15:
                toaster.show_toast(
                    "Carpeta Actualizada",
                    f"La carpeta {identifier} ha sido actualizada recientemente.",
                    duration=5  # Tiempo de visualización reducido
                )
            elif time_difference > 20:
                toaster.show_toast(
                    "Carpeta Desactualizada",
                    f"La carpeta {identifier} no se ha actualizado en más de 20 minutos.",
                    duration=5  # Tiempo de visualización reducido
                )
            results.append(f"La carpeta {identifier} existe. Última modificación: {formatted_mod_time}")
        else:
            results.append(f"La carpeta {identifier} no existe")

    # Programar la actualización de la GUI en el hilo principal
    root.after(0, update_result_text, results)

def update_result_text(results):
    result_text.delete(1.0, tk.END)
    for result in results:
        result_text.insert(tk.END, result + "\n")

def update_ui():
    folder_listbox.delete(0, tk.END)
    for folder_path in folder_paths:
        folder_listbox.insert(tk.END, folder_path)

def schedule_check():
    global checking
    checking = True
    threading.Thread(target=check_folder).start()
    try:
        interval = int(interval_entry.get())
    except ValueError:
        interval = 15  # Valor por defecto si la entrada no es válida
    if checking:
        root.after(interval * 60 * 1000, schedule_check)  # Programar la siguiente comprobación

def stop_check():
    global checking
    checking = False

def exit_app():
    root.quit()

# Crear la ventana principal
root = tk.Tk()
root.title("Comprobar Carpetas")

# Crear un botón para agregar carpetas
add_button = tk.Button(root, text="Agregar Carpeta", command=add_folder)
add_button.pack(pady=5)

# Crear un botón para eliminar carpetas
remove_button = tk.Button(root, text="Eliminar Carpeta", command=remove_folder)
remove_button.pack(pady=5)

# Crear una lista para mostrar las carpetas
folder_listbox = tk.Listbox(root, height=10, width=80)
folder_listbox.pack(pady=10)

# Crear un campo de entrada para el intervalo de minutos
interval_label = tk.Label(root, text="Intervalo de minutos para la comprobación:")
interval_label.pack(pady=5)
interval_entry = tk.Entry(root)
interval_entry.pack(pady=5)
interval_entry.insert(0, "15")  # Valor por defecto

# Crear un botón para iniciar la comprobación periódica
check_button = tk.Button(root, text="Comprobar Carpetas", command=schedule_check)
check_button.pack(pady=10)

# Crear un botón para detener la comprobación
stop_button = tk.Button(root, text="Detener Comprobación", command=stop_check)
stop_button.pack(pady=5)

# Crear un botón para salir de la aplicación
exit_button = tk.Button(root, text="Salir", command=exit_app)
exit_button.pack(pady=5)

# Crear un widget de texto para mostrar los resultados
result_text = tk.Text(root, height=10, width=80)
result_text.pack(pady=10)

# Ejecutar el bucle principal de la UI
root.mainloop()