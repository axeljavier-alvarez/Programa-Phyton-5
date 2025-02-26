import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
#instalar calendario pip install tkcalendar view/toolwindows/terminal
tree = ttk.Treeview
#donde se guardara
DATA_FILE = "tareas.txt"

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

#FUNCION PARA AGREGAR
def agregar_tareas():
    def agregar():
        vnombre = nombre.get()
        vestado = "Pendiente"
        vdescripcion = descripcion.get()
        vfecha = fecha.get()

        # Verificar que todos los campos estén completos
        if not vnombre or not vdescripcion or not vfecha:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        try:
            with open(DATA_FILE, "a") as file:
                file.write(f"{vnombre},{vestado},{vdescripcion},{vfecha}\n")
                messagebox.showinfo("Tarea Agregada", "La tarea fue agregada exitosamente")
        except FileNotFoundError:
            print(f"Error: El archivo {file} no fue encontrado")

    window_agregar_tareas = tk.Toplevel(root)
    window_agregar_tareas.title("Agregar tareas")
    window_agregar_tareas.geometry("600x300")

    # Crear las etiquetas y campos de entrada
    label_nombre = tk.Label(window_agregar_tareas, text="Introduce el nombre:")
    label_nombre.grid(row=0, column=0, padx=10, pady=10)
    nombre = tk.Entry(window_agregar_tareas)
    nombre.grid(row=0, column=1, padx=10, pady=10)
    nombre.bind("<Return>", focus_next_widget)

    label_descripcion = tk.Label(window_agregar_tareas, text="Descripción:")
    label_descripcion.grid(row=1, column=0, padx=10, pady=10)
    descripcion = tk.Entry(window_agregar_tareas)
    descripcion.grid(row=1, column=1, padx=10, pady=10)

    label_fecha = tk.Label(window_agregar_tareas, text="Fecha:")
    label_fecha.grid(row=2, column=0, padx=10, pady=10)
    fecha = DateEntry(window_agregar_tareas, width=16, background='darkblue', foreground='white', borderwidth=2)  # Calendario
    fecha.grid(row=2, column=1, padx=10, pady=10)

    button = tk.Button(window_agregar_tareas, text="Agregar", command=agregar)
    button.grid(row=3, column=0, columnspan=2, pady=10)

#FUNCION PARA VER TAREAS
def ver_tareas():
    def load_list():
        data = leer_tareas()

        for row in tree.get_children():
            tree.delete(row)

        for item in data:
            tree.insert("", "end", values=item)

    window_ver_tareas = tk.Toplevel(root)
    window_ver_tareas.title("Ver tareas")
    window_ver_tareas.geometry("900x300")
    tareas = leer_tareas()

    # Crear el Treeview con columnas adicionales
    columns = ("Nombre", "Estado", "Descripción", "Fecha")
    tree = ttk.Treeview(window_ver_tareas, columns=columns, show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Estado", text="Estado")
    tree.heading("Descripción", text="Descripción")
    tree.heading("Fecha", text="Fecha")
    tree.grid(row=0, column=0, sticky="nsew")

    # Añadir una barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(window_ver_tareas, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Configurar el grid
    window_ver_tareas.grid_rowconfigure(0, weight=1)
    window_ver_tareas.grid_columnconfigure(0, weight=1)


#Boton opcional, lo puedo quitar si quiero
    button2 = tk.Button(window_ver_tareas, text="Cargar Lista", command=load_list)
    button2.grid(row=2, column=1, pady=10)

#Cargar datos automaticamente
    load_list()

def leer_tareas():
    if not os.path.exists(DATA_FILE):
        return []
    tareas = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            nombre, estado, descripcion, fecha = line.strip().split(",")
            tareas.append((nombre, estado, descripcion, fecha))
    return tareas

#FUNCION PARA ELIMINAR TAREAS
def eliminar_tareas():
    def eliminar():
        vnumero = int(numero.get())
        if (vnumero >= 1) and (vnumero <= len(tareas)):
            # Elimina una tarea de la lista basada en un índice proporcionado por el usuario
            tareas.pop(vnumero - 1)
            guardar_tareas(tareas)
            messagebox.showinfo("Tarea Eliminada", "La tarea fue eliminada exitosamente")
            # Cargar lista luego de eliminar un elemento
            load_list()
        else:
            messagebox.showerror("Error", "Número de tarea inválido")

    # Función para cargar la lista en el Treeview
    def load_list():
        data = leer_tareas()

        for row in tree.get_children():
            tree.delete(row)

        for idx, item in enumerate(data, start=1):
            tree.insert("", "end", values=(idx, *item))

    window_eliminar_tareas = tk.Toplevel(root)
    window_eliminar_tareas.title("Eliminar Tarea")
    window_eliminar_tareas.geometry("900x300")
    tareas = leer_tareas()

    # Agregar etiqueta y campo para indicar el número de tarea a borrar
    label = tk.Label(window_eliminar_tareas, text="Introduce el número de tarea: ")
    label.grid(row=1, column=0, padx=10, pady=10)

    # Crear un cuadro de texto para el número
    numero = tk.Entry(window_eliminar_tareas)
    numero.grid(row=1, column=1, padx=10, pady=10)
    numero.bind("<Return>", focus_next_widget)

    # Crear el Treeview con columnas adicionales
    columns = ("Número", "Nombre", "Estado", "Descripción", "Fecha")
    tree = ttk.Treeview(window_eliminar_tareas, columns=columns, show="headings")
    tree.heading("Número", text="Número")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Estado", text="Estado")
    tree.heading("Descripción", text="Descripción")
    tree.heading("Fecha", text="Fecha")
    tree.grid(row=0, column=0, sticky="nsew")

    # Añadir una barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(window_eliminar_tareas, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Configurar el grid
    window_eliminar_tareas.grid_rowconfigure(0, weight=0)
    window_eliminar_tareas.grid_columnconfigure(0, weight=1)

    # Botón para eliminar la tarea
    button = tk.Button(window_eliminar_tareas, text="Eliminar", command=eliminar)
    button.grid(row=2, column=0, pady=10)

    # Botón para cargar la lista
    button2 = tk.Button(window_eliminar_tareas, text="Cargar Lista", command=load_list)
    button2.grid(row=2, column=1, pady=10)

    # Cargar tareas automáticamente
    load_list()

def guardar_tareas(tareas):
    with open(DATA_FILE, "w") as file:
        for contacto in tareas:
            file.write(",".join(contacto)+"\n")

#FUNCIONES FALTANTES:
#1. Asignar una tarea por medio del numero
def cambiar_estado():
    def cambiar():
        vnumero = int(numero.get())
        if (vnumero >= 1) and (vnumero <= len(tareas)):
            nombre, estado, descripcion, fecha = tareas[vnumero - 1]
            if estado == "Completada":
                messagebox.showwarning("Advertencia", "Esta tarea ya está completada y no se puede cambiar.")
            else:
                tareas[vnumero - 1] = (nombre, "Completada", descripcion, fecha)
                guardar_tareas(tareas)
                messagebox.showinfo("Estado Cambiado", "La tarea ha sido marcada como completada.")
                load_list()
        else:
            messagebox.showerror("Error", "Número de tarea inválido")

    # Cargar la lista en el Treeview
    def load_list():
        data = leer_tareas()

        for row in tree.get_children():
            tree.delete(row)

        for idx, item in enumerate(data, start=1):
            tree.insert("", "end", values=(idx, *item))  # Agregar índice como número

    window_cambiar_estado = tk.Toplevel(root)
    window_cambiar_estado.title("Cambiar Estado")
    window_cambiar_estado.geometry("900x300")
    tareas = leer_tareas()

    label = tk.Label(window_cambiar_estado, text="Introduce el número de la tarea:")
    label.grid(row=1, column=0, padx=10, pady=10)

    numero = tk.Entry(window_cambiar_estado)
    numero.grid(row=1, column=1, padx=10, pady=10)
    numero.bind("<Return>", focus_next_widget)

    # Crear el Treeview con columnas adicionales
    columns = ("Número", "Nombre", "Estado", "Descripción", "Fecha")
    tree = ttk.Treeview(window_cambiar_estado, columns=columns, show="headings")
    tree.heading("Número", text="Número")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Estado", text="Estado")
    tree.heading("Descripción", text="Descripción")
    tree.heading("Fecha", text="Fecha")
    tree.grid(row=0, column=0, sticky="nsew")

    # Añadir una barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(window_cambiar_estado, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Configurar el grid
    window_cambiar_estado.grid_rowconfigure(0, weight=0)
    window_cambiar_estado.grid_columnconfigure(0, weight=1)

    button = tk.Button(window_cambiar_estado, text="Cambiar Estado", command=cambiar)
    button.grid(row=2, column=0, pady=10)

    # Botón para cargar la lista
    button2 = tk.Button(window_cambiar_estado, text="Cargar Lista", command=load_list)
    button2.grid(row=2, column=1, pady=10)

    # Cargar automáticamente la lista de tareas al abrir la ventana
    load_list()

#2. Editar tarea
def editar_tarea():
    def editar():
        try:
            vnumero = int(numero.get())
            if (vnumero >= 1) and (vnumero <= len(tareas)):
                new_name = nuevo_nombre.get()
                tareas[vnumero - 1] = (new_name, tareas[vnumero - 1][1], tareas[vnumero - 1][2], tareas[vnumero - 1][3])
                guardar_tareas(tareas)
                messagebox.showinfo("Tarea Editada", "El nombre de la tarea ha sido actualizado.")
                load_list()  # Cargar la lista después de editar
            else:
                messagebox.showerror("Error", "Número de tarea inválido.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un número válido.")

    def load_list():
        data = leer_tareas()
        for row in tree.get_children():
            tree.delete(row)
        for idx, item in enumerate(data, start=1):
            tree.insert("", "end", values=(idx, *item))  # Agregar índice como número

    window_editar_tarea = tk.Toplevel(root)
    window_editar_tarea.title("Editar Tarea")
    window_editar_tarea.geometry("600x300")
    tareas = leer_tareas()

    label = tk.Label(window_editar_tarea, text="Introduce el número de la tarea:")
    label.pack(pady=10)

    numero = tk.Entry(window_editar_tarea, width=30)  # Ajustar tamaño
    numero.pack(pady=10)

    label_nuevo = tk.Label(window_editar_tarea, text="Introduce el nuevo nombre:")
    label_nuevo.pack(pady=10)

    nuevo_nombre = tk.Entry(window_editar_tarea, width=30)  # Ajustar tamaño
    nuevo_nombre.pack(pady=10)

    # Crear un frame para los botones
    button_frame = tk.Frame(window_editar_tarea)
    button_frame.pack(pady=10)

    button = tk.Button(button_frame, text="Editar Tarea", command=editar)
    button.pack(side=tk.LEFT, padx=5)  # Alinear a la izquierda

    # Botón para cargar la lista
    button2 = tk.Button(button_frame, text="Cargar Lista", command=load_list)
    button2.pack(side=tk.LEFT, padx=5)  # Alinear a la izquierda

    # Crear el Treeview con columnas adicionales
    columns = ("Número", "Nombre", "Estado", "Descripción", "Fecha")
    global tree  # Hacer 'tree' global para poder usarlo en 'load_list'
    tree = ttk.Treeview(window_editar_tarea, columns=columns, show="headings")
    tree.heading("Número", text="Número")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Estado", text="Estado")
    tree.heading("Descripción", text="Descripción")
    tree.heading("Fecha", text="Fecha")
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Añadir una barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(window_editar_tarea, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    load_list()

# 3. Mostrar tareas completadas
def mostrar_completadas():
    def load_list():
        data = [tarea for tarea in tareas if tarea[1] == "Completada"]
        for row in tree.get_children():
            tree.delete(row)
        for item in data:
            tree.insert("", "end", values=item)

    window_mostrar_completadas = tk.Toplevel(root)
    window_mostrar_completadas.title("Tareas Completadas")
    window_mostrar_completadas.geometry("600x300")
    tareas = leer_tareas()

    columns = ("Nombre", "Estado")
    tree = ttk.Treeview(window_mostrar_completadas, columns=columns, show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Estado", text="Estado")
    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(window_mostrar_completadas, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    window_mostrar_completadas.grid_rowconfigure(0, weight=0)
    window_mostrar_completadas.grid_columnconfigure(0, weight=1)

    button2 = tk.Button(window_mostrar_completadas, text="Cargar Completadas", command=load_list)
    button2.grid(row=1, column=0, pady=10)
    load_list()


# Menu principal
# Ventana principal

root = tk.Tk()
root.title("Ventana principal")
root.geometry("500x500")

#Crear la barra del menú
menu_bar = Menu(root)
root.config(menu=menu_bar)

#Agregar un menú despegable
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="archivo", menu=file_menu)

#Aqui se van agregando las funciones
file_menu.add_command(label="Agregar Tareas", command=agregar_tareas)
file_menu.add_command(label="Ver Tareas", command=ver_tareas)
file_menu.add_command(label="Eliminar Tareas", command=eliminar_tareas)
file_menu.add_command(label="Cambiar Estado", command=cambiar_estado)
file_menu.add_command(label="Editar Tarea", command=editar_tarea)
file_menu.add_command(label="Mostrar Tareas Completadas", command=mostrar_completadas)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)
root.mainloop()



"""
root = tk.Tk()
root.title("Ventana Principal")
root.geometry("500x500")
# CONFIGURANDO FONDO
root.configure(bg="#2E2E2E")

#AGREGANDO EL TITULO
titulo = tk.Label(root, text="Administración de Tareas", bg="#2E2E2E", fg="white", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Crear un marco para los botones
frame = tk.Frame(root, bg="#2E2E2E")
frame.pack(pady=20)

# Colores recomendados
button_add_bg = "#28A745"
button_edit_bg = "#FFC107"
button_delete_bg = "#DC3545"
button_fg = "#FFFFFF"
button_hover_bg = "#0056b3"

# Función para cambiar el color al pasar el ratón

def on_enter(e):
    e.widget['background'] = button_hover_bg

def on_leave(e):
    # Restablecer color según el tipo de botón
    if e.widget['text'] == "Agregar Tareas":
        e.widget['background'] = button_add_bg
    elif e.widget['text'] == "Editar Tarea":
        e.widget['background'] = button_edit_bg
    elif e.widget['text'] == "Eliminar Tareas":
        e.widget['background'] = button_delete_bg
    else:
        e.widget['background'] = "#007BFF"  # Color genérico

# Crear botones
buttons = [
    ("Agregar Tareas", agregar_tareas, button_add_bg),
    ("Ver Tareas", ver_tareas, "#007BFF"),  # Azul genérico
    ("Eliminar Tareas", eliminar_tareas, button_delete_bg),
    ("Cambiar Estado", cambiar_estado, "#007BFF"),
    ("Editar Tarea", editar_tarea, button_edit_bg),
    ("Mostrar Tareas Completadas", mostrar_completadas, "#007BFF"),
    ("Salir", root.quit, "#007BFF")
]


for (text, command, bg_color) in buttons:
    button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=button_fg, width=25, height=2)
    button.pack(pady=5)
    
    button.bind("<Enter>", on_enter)
    
    button.bind("<Leave>", on_leave) 

root.mainloop()
"""