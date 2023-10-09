import tkinter as tk
from tkinter import *
import csv
from tkinter import messagebox


# Colores
fondo_entrar = "#FFFFFF"
fondo_salir = "#FFFFFF"
fondo_correcto = "#FFFFFF"
fondo_incorrecto = "#FFFFFF"
fondo_entrada = "#FFFFFF"

class Libro:
    def __init__(self, titulo, autor, genero, anio_publicacion, estado):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.estado = estado
        self.reservado = False  # Agrega esta propiedad para rastrear la reserva

    def reservar(self):
        self.reservado = True

    def cancelar_reserva(self):
        self.reservado = False

class Biblioteca:
    def __init__(self):
        self.libros = []
        self.archivo_csv = 'biblioteca.csv'

        self.leer_csv()

    def leer_csv(self):
        try:
            with open(self.archivo_csv, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    titulo, autor, genero, anio_publicacion, estado = row
                    libro = Libro(titulo, autor, genero, anio_publicacion, estado)

                    # Verificar si el estado indica que el libro está reservado
                    if estado.lower() == "reservado":
                        libro.reservar()  # Establecer el estado de reserva

                    self.libros.append(libro)
        except FileNotFoundError:
            pass

    def guardar_csv(self):
        try:
            with open(self.archivo_csv, mode='w', newline='') as file:
                writer = csv.writer(file)
                for libro in self.libros:
                    writer.writerow([libro.titulo, libro.autor, libro.genero, libro.anio_publicacion, libro.estado])
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo guardar en el archivo CSV: {e}")


def hide_me(event):
    event.widget.pack_forget()

def login():
    nombre = usuario.get()
    contrasena = password.get()
    if (nombre == "admi" or nombre == "Mike") and contrasena == "admi":
        correcta()
    else:
        incorrecta()

def create_main_window():
    global ventana_biblioteca  # Agrega esta línea para acceder a la variable global

    window = tk.Toplevel()
    window.title("Biblioteca")
    window.geometry("500x500+500+50")
    window.resizable(width=False, height=False)
    fondo = tk.PhotoImage(file="Bienvenido.png")
    fondo1 = tk.Label(window, image=fondo)
    fondo1.place(x=0, y=0, relwidth=1, relheight=1)

    ventana_biblioteca = window  # Actualiza la referencia a la ventana de biblioteca

    return window

def create_button(parent, text, command, y_position, x_position):
    boton = tk.Button(parent, text=text, command=command, cursor="hand2", relief="flat", bg=fondo_correcto, font=("Comic Sans MS", 12, "bold"), activebackground="red")
    boton.place(x=x_position, y=y_position)


def correcta():
    nombre = usuario.get()
    ventana.withdraw()
    window = create_main_window()

    # Carga la imagen de fondo
    fondo = tk.PhotoImage(file="bienvenido.png")

    # Crea un Label para mostrar la imagen de fondo
    imagen_bienvenida = tk.Label(window, image=fondo)
    imagen_bienvenida.photo = fondo  # Mantén una referencia local a la imagen

    # Coloca el Label en la ventana
    imagen_bienvenida.place(x=0, y=0, relwidth=1, relheight=1)

    mensaje_bienvenida = tk.Label(window, text=f"Bienvenido, {nombre} Al SAB", font=("Comic Sans MS", 21, "bold"), bg="#DADADA")
    mensaje_bienvenida.place(x=20, y=30)


    def regreso():
        window.withdraw()
        ventana.deiconify()


    create_button(window, "Agregar", agregar_libro, y_position=130, x_position=110)
    create_button(window, "Biblioteca", mostrar_libros, y_position=130, x_position=350)
    create_button(window, "Buscar", buscar_libros, y_position=220, x_position=110)
    create_button(window, "Reservar", reservar_libros, y_position=220, x_position=350)
    create_button(window, "Cancelar R. ", cancelar_reserva, y_position=320, x_position=110)
    create_button(window, "Actualizar", actualizar_libro, y_position=320, x_position=350)
    create_button(window, "Eliminar libro", eliminar_libro, y_position=410, x_position=110)
    create_button(window, "Salir", regreso, y_position=410, x_position=350)


def agregar_libro():
    ventana.withdraw()
    root = tk.Toplevel()
    root.title("Agregar Libro")
    root.geometry("600x500")
    root.resizable(width=False, height=False)
    fondo = tk.PhotoImage(file="error.png")
    fondo1 = tk.Label(root, image=fondo)
    fondo1.place(x=0, y=0, relwidth=1, relheight=1)

    # Variables para almacenar la información del libro
    titulo_var = tk.StringVar()
    autor_var = tk.StringVar()
    genero_var = tk.StringVar()
    anio_var = tk.StringVar()

    # Función para guardar la información del libro en el archivo CSV
    def guardar_csv():
        try:
            with open(biblioteca.archivo_csv, mode='w', newline='') as file:
                writer = csv.writer(file)
                for libro in biblioteca.libros:
                    writer.writerow([libro.titulo, libro.autor, libro.genero, libro.anio_publicacion, libro.estado])
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo guardar en el archivo CSV: {e}")

    ventana_biblioteca = None

    # Función para guardar un nuevo libro en la biblioteca
    def guardar_libro():
        titulo = titulo_var.get()
        autor = autor_var.get()
        genero = genero_var.get()
        anio_publicacion = anio_var.get()

        # Validar que se haya ingresado al menos el título
        if not titulo:
            tk.messagebox.showerror("Error", "Debe ingresar al menos el título del libro.")
            return

        # Crear una instancia de Libro y agregarla a la biblioteca
        nuevo_libro = Libro(titulo, autor, genero, anio_publicacion, "Disponible")
        biblioteca.libros.append(nuevo_libro)

        # Guardar los datos en el archivo CSV
        guardar_csv()

        messagebox.showinfo("Éxito", f"El libro '{titulo}' se ha agregado correctamente.")
        root.destroy()
        ventana_biblioteca.deiconify()

    # Etiquetas y entradas para la información del libro
    tk.Label(root, text="Título:", font=("Comic Sans MS", 14)).place(x=50, y=100)
    titulo_entry = tk.Entry(root, textvar=titulo_var, font=("Comic Sans MS", 14), width=30)
    titulo_entry.place(x=200, y=100)

    tk.Label(root, text="Autor:", font=("Comic Sans MS", 14)).place(x=50, y=150)
    autor_entry = tk.Entry(root, textvar=autor_var, font=("Comic Sans MS", 14), width=30)
    autor_entry.place(x=200, y=150)

    tk.Label(root, text="Género:", font=("Comic Sans MS", 14)).place(x=50, y=200)
    genero_entry = tk.Entry(root, textvar=genero_var, font=("Comic Sans MS", 14), width=30)
    genero_entry.place(x=200, y=200)

    tk.Label(root, text="Año de Publicación:", font=("Comic Sans MS", 14)).place(x=50, y=250)
    anio_entry = tk.Entry(root, textvar=anio_var, font=("Comic Sans MS", 14), width=10)
    anio_entry.place(x=250, y=250)

    # Botón para guardar el libro
    guardar_button = tk.Button(root, text="Guardar", command=guardar_libro, cursor="hand2", relief="flat", bg=fondo_correcto,font=("Comic Sans MS", 16, "bold"), activebackground="red")
    guardar_button.place(x=250, y=350)

    # Botón para volver atrás
    def atras():
        root.destroy()
        ventana_biblioteca.deiconify()

    boton_atras = tk.Button(root, text="Atrás", command=atras, cursor="hand2", relief="flat", bg=fondo_correcto,font=("Comic Sans MS", 16, "bold"), activebackground="red")
    boton_atras.place(x=50, y=350)

def mostrar_libros():
    ventana.withdraw()  # Oculta la ventana principal

    # Crea una nueva ventana para mostrar los libros
    window = tk.Toplevel()
    window.title("Lista de Libros")
    window.geometry("600x400+500+50")
    window.resizable(width=False, height=False)

    # Agrega un cuadro de texto para mostrar la información de los libros
    libro_text = tk.Text(window, font=("Comic Sans MS", 12), wrap=tk.WORD)
    libro_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Llena el cuadro de texto con la información de los libros (omitir la primera fila)
    for libro in biblioteca.libros[1:]:  # Omitir la primera fila (encabezados)
        libro_text.insert(tk.END, f"Título: {libro.titulo}\n")
        libro_text.insert(tk.END, f"Autor: {libro.autor}\n")
        libro_text.insert(tk.END, f"Género: {libro.genero}\n")
        libro_text.insert(tk.END, f"Año de Publicación: {libro.anio_publicacion}\n")
        libro_text.insert(tk.END, f"Estado: {libro.estado}\n")
        libro_text.insert(tk.END, "-"*50 + "\n")  # Separador

    def regresar():
        window.destroy()  # Cierra la ventana de lista de libros
        ventana.deiconify()  # Muestra la ventana principal nuevamente

    # Botón para regresar
    boton_regresar = tk.Button(window, text="Regresar", command=regresar, cursor="hand2", relief="flat", bg=fondo_correcto, font=("Comic Sans MS", 14, "bold"), activebackground="red")
    boton_regresar.pack(pady=10)

def buscar_libros():
    # Función para realizar la búsqueda de libros por autor
    def mostrar_resultados(resultados):
        # Crea una ventana emergente para mostrar los resultados
        ventana_resultados = tk.Toplevel()
        ventana_resultados.title("Resultados de la Búsqueda")
        ventana_resultados.geometry("400x400+500+50")
        ventana_resultados.resizable(width=False, height=False)

        # Agrega un cuadro de texto para mostrar los resultados
        resultados_text = tk.Text(ventana_resultados, font=("Comic Sans MS", 12), wrap=tk.WORD)
        resultados_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Muestra los resultados en el cuadro de texto
        for libro in resultados:
            resultados_text.insert(tk.END, f"Título: {libro.titulo}\n")
            resultados_text.insert(tk.END, f"Autor: {libro.autor}\n")
            resultados_text.insert(tk.END, f"Género: {libro.genero}\n")
            resultados_text.insert(tk.END, f"Año de Publicación: {libro.anio_publicacion}\n")
            resultados_text.insert(tk.END, f"Estado: {libro.estado}\n")
            resultados_text.insert(tk.END, "-" * 50 + "\n")  # Separador

        # Botón para cerrar la ventana de resultados
        def cerrar_ventana():
            ventana_resultados.destroy()

        cerrar_button = tk.Button(ventana_resultados, text="Cerrar", command=cerrar_ventana, cursor="hand2",
                                  relief="flat", bg=fondo_correcto, font=("Comic Sans MS", 14, "bold"),
                                  activebackground="red")
        cerrar_button.pack(pady=10)

        # Asegúrate de que la ventana de resultados permanezca abierta
        ventana_resultados.mainloop()
    def realizar_busqueda():
        autor_busqueda = autor_entry.get().strip()

        if not autor_busqueda:
            messagebox.showerror("Error", "Por favor, ingrese el nombre del autor.")
            return

        resultados = []

        for libro in biblioteca.libros:
            if libro.autor.lower() == autor_busqueda.lower():
                resultados.append(libro)

        if not resultados:
            messagebox.showinfo("Resultados", f"No se encontraron libros del autor '{autor_busqueda}'.")
        else:
            # Mostrar los resultados en una nueva ventana emergente
            mostrar_resultados(resultados)

    # Ocultar la ventana principal
    ventana.withdraw()

    # Crear una nueva ventana para la búsqueda por autor
    ventana_busqueda = tk.Toplevel()
    ventana_busqueda.title("Buscar Libros por Autor")
    ventana_busqueda.geometry("400x200+500+50")
    ventana_busqueda.resizable(width=False, height=False)

    # Etiqueta y entrada para ingresar el autor
    tk.Label(ventana_busqueda, text="Autor:", font=("Comic Sans MS", 14)).place(x=30, y=40)
    autor_entry = tk.Entry(ventana_busqueda, font=("Comic Sans MS", 14), width=20)
    autor_entry.place(x=120, y=40)

    # Botón para realizar la búsqueda
    buscar_button = tk.Button(ventana_busqueda, text="Buscar", command=realizar_busqueda, cursor="hand2", relief="flat", bg=fondo_correcto, font=("Comic Sans MS", 14, "bold"), activebackground="red")
    buscar_button.place(x=160, y=100)

    # Botón para regresar a la ventana principal de Biblioteca
    def regresar():
        ventana_busqueda.destroy()
        ventana_biblioteca.deiconify()  # Muestra la ventana de biblioteca existente

    regresar_button = tk.Button(ventana_busqueda, text="Regresar", command=regresar, cursor="hand2", relief="flat", bg=fondo_correcto, font=("Comic Sans MS", 14, "bold"), activebackground="red")
    regresar_button.place(x=30, y=150)

    ventana_busqueda.mainloop()

def reservar_libros():
    # Crea una nueva ventana para el menú de opciones
    ventana_reservar_libros = tk.Toplevel()
    ventana_reservar_libros.title("Reservar Libros")
    ventana_reservar_libros.geometry("400x400+500+50")
    ventana_reservar_libros.resizable(width=False, height=False)

    # Crea una lista de libros disponibles que no están reservados
    libros_disponibles = [libro for libro in biblioteca.libros if libro.estado == "Disponible" or "disponible"]

    if not libros_disponibles:
        tk.Label(ventana_reservar_libros, text="No hay libros disponibles para reservar.", font=("Comic Sans MS", 14)).pack(pady=20)
    else:
        tk.Label(ventana_reservar_libros, text="Selecciona los libros que deseas reservar:", font=("Comic Sans MS", 14)).pack(pady=10)

        # Lista de control de selección de libros
        libros_seleccionados = []

        # Función para manejar la selección/deselección de libros
        def toggle_seleccion(libro):
            if libro in libros_seleccionados:
                libros_seleccionados.remove(libro)
            else:
                libros_seleccionados.append(libro)

        # Crea un conjunto de variables tkinter para las casillas de verificación
        checkbox_vars = [tk.IntVar() for _ in libros_disponibles]

        # Crea las casillas de verificación para cada libro disponible
        for i, libro in enumerate(libros_disponibles):
            libro_checkbox = tk.Checkbutton(ventana_reservar_libros, text=libro.titulo,
                                            variable=checkbox_vars[i], onvalue=1, offvalue=0,
                                            command=lambda i=i, libro=libro: toggle_seleccion(libro))
            libro_checkbox.pack(anchor="w")

        def realizar_reserva():
            if libros_seleccionados:
                for libro in libros_seleccionados:
                    libro.reservar()
                    libro.estado = "Reservado"
                biblioteca.guardar_csv()
                messagebox.showinfo("Éxito", f"Se han reservado los libros seleccionados.")
                ventana_reservar_libros.destroy()
            else:
                messagebox.showwarning("Ningún libro seleccionado", "Por favor, selecciona al menos un libro para reservar.")

        # Botón para realizar la reserva con la selección actual
        reservar_button = tk.Button(ventana_reservar_libros, text="Reservar Libros", command=realizar_reserva,
                                    cursor="hand2", relief="flat", bg="#33FF33", font=("Comic Sans MS", 14, "bold"), activebackground="green")
        reservar_button.pack(pady=10)

# ... (código posterior) ...



def cancelar_reserva():
    # Crea una nueva ventana para el menú de opciones
    ventana_cancelar_reserva = tk.Toplevel()
    ventana_cancelar_reserva.title("Cancelar Reserva")
    ventana_cancelar_reserva.geometry("400x300+500+50")
    ventana_cancelar_reserva.resizable(width=False, height=False)

    # Crea una lista de libros reservados
    libros_reservados = [libro for libro in biblioteca.libros if libro.reservado]

    if not libros_reservados:
        tk.Label(ventana_cancelar_reserva, text="No hay libros reservados.", font=("Comic Sans MS", 14)).pack(pady=20)
    else:
        tk.Label(ventana_cancelar_reserva, text="Selecciona un libro a cancelar la reserva:",
                 font=("Comic Sans MS", 14)).pack(pady=10)

        # Lista desplegable para mostrar los libros reservados
        libro_seleccionado = tk.StringVar(ventana_cancelar_reserva)
        libro_seleccionado.set(libros_reservados[0].titulo)  # Establece el primer libro como predeterminado

        libro_dropdown = tk.OptionMenu(ventana_cancelar_reserva, libro_seleccionado,
                                       *[libro.titulo for libro in libros_reservados])
        libro_dropdown.pack(pady=10)

        def realizar_cancelacion():
            titulo_seleccionado = libro_seleccionado.get()

            for libro in libros_reservados:
                if libro.titulo == titulo_seleccionado:
                    # Crea una ventana emergente de confirmación
                    confirmacion = messagebox.askyesno("Confirmar Cancelación",
                                                       f"¿Estás seguro de que deseas cancelar la reserva del libro '{libro.titulo}'?")

                    if confirmacion:
                        libro.cancelar_reserva()
                        libro.estado = "Disponible"
                        biblioteca.guardar_csv()
                        messagebox.showinfo("Éxito", f"Se ha cancelado la reserva del libro '{libro.titulo}'.")
                        ventana_cancelar_reserva.destroy()
                    else:
                        messagebox.showinfo("Cancelación Cancelada",
                                            f"No se ha cancelado la reserva del libro '{libro.titulo}'.")
                    break

        # Botón para realizar la cancelación con confirmación
        cancelar_button = tk.Button(ventana_cancelar_reserva, text="Cancelar Reserva", command=realizar_cancelacion,
                                    cursor="hand2",
                                    relief="flat", bg="#FF5733", font=("Comic Sans MS", 14, "bold"),
                                    activebackground="red")
        cancelar_button.pack(pady=10)
def actualizar_libro():
    # Ventana emergente para seleccionar un libro de la biblioteca
    ventana_actualizar = tk.Toplevel()
    ventana_actualizar.title("Actualizar Libro")
    ventana_actualizar.geometry("500x500")
    ventana_actualizar.resizable(width=False, height=False)

    tk.Label(ventana_actualizar, text="Selecciona un libro:", font=("Comic Sans MS", 14)).pack(pady=10)

    # Lista desplegable para mostrar los títulos de los libros
    libros_disponibles = [libro.titulo for libro in biblioteca.libros if not libro.reservado]
    libro_seleccionado = tk.StringVar(ventana_actualizar)
    libro_seleccionado.set(libros_disponibles[0])  # Establece el primer libro como predeterminado

    libro_dropdown = tk.OptionMenu(ventana_actualizar, libro_seleccionado, *libros_disponibles)
    libro_dropdown.pack()

    # Entradas para actualizar la información del libro
    tk.Label(ventana_actualizar, text="Nuevo Título:", font=("Comic Sans MS", 14)).pack(pady=10)
    nuevo_titulo_entry = tk.Entry(ventana_actualizar, font=("Comic Sans MS", 12), width=30)
    nuevo_titulo_entry.pack()

    tk.Label(ventana_actualizar, text="Nuevo Autor:", font=("Comic Sans MS", 14)).pack(pady=10)
    nuevo_autor_entry = tk.Entry(ventana_actualizar, font=("Comic Sans MS", 12), width=30)
    nuevo_autor_entry.pack()

    tk.Label(ventana_actualizar, text="Nuevo Género:", font=("Comic Sans MS", 14)).pack(pady=10)
    nuevo_genero_entry = tk.Entry(ventana_actualizar, font=("Comic Sans MS", 12), width=30)
    nuevo_genero_entry.pack()

    tk.Label(ventana_actualizar, text="Nuevo Año de Publicación:", font=("Comic Sans MS", 14)).pack(pady=10)
    nuevo_anio_entry = tk.Entry(ventana_actualizar, font=("Comic Sans MS", 12), width=10)
    nuevo_anio_entry.pack()

    def realizar_actualizacion():
        # Obtener el título seleccionado y el libro correspondiente
        titulo_seleccionado = libro_seleccionado.get()
        libro_actualizar = None

        for libro in biblioteca.libros:
            if libro.titulo == titulo_seleccionado:
                libro_actualizar = libro
                break

        if libro_actualizar:
            # Obtener los nuevos valores de los campos
            nuevo_titulo = nuevo_titulo_entry.get()
            nuevo_autor = nuevo_autor_entry.get()
            nuevo_genero = nuevo_genero_entry.get()
            nuevo_anio = nuevo_anio_entry.get()

            # Actualizar la información del libro
            if nuevo_titulo:
                libro_actualizar.titulo = nuevo_titulo
            if nuevo_autor:
                libro_actualizar.autor = nuevo_autor
            if nuevo_genero:
                libro_actualizar.genero = nuevo_genero
            if nuevo_anio:
                libro_actualizar.anio_publicacion = nuevo_anio

            # Actualizar el archivo CSV
            biblioteca.guardar_csv()

            messagebox.showinfo("Éxito", f"El libro '{titulo_seleccionado}' se ha actualizado correctamente.")
            ventana_actualizar.destroy()
        else:
            messagebox.showerror("Error", f"No se pudo encontrar el libro '{titulo_seleccionado}'.")

    tk.Button(ventana_actualizar, text="Actualizar Libro", command=realizar_actualizacion, cursor="hand2",
              relief="flat", bg=fondo_correcto, font=("Comic Sans MS", 14, "bold"), activebackground="red").pack(pady=10)

    ventana_actualizar.mainloop()


def eliminar_libro():
    # Ocultar la ventana principal
    ventana.withdraw()

    # Crear una nueva ventana para la eliminación de libros
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Libro")
    ventana_eliminar.geometry("400x200+500+50")
    ventana_eliminar.resizable(width=False, height=False)

    # Etiqueta y lista desplegable para seleccionar el libro a eliminar
    tk.Label(ventana_eliminar, text="Seleccione el libro a eliminar:", font=("Comic Sans MS", 14)).pack(pady=10)

    libros_disponibles = [libro.titulo for libro in biblioteca.libros if not libro.reservado]
    libro_seleccionado = tk.StringVar(ventana_eliminar)
    libro_seleccionado.set(libros_disponibles[0])  # Establece el primer libro como predeterminado

    libro_dropdown = tk.OptionMenu(ventana_eliminar, libro_seleccionado, *libros_disponibles)
    libro_dropdown.pack()

    # Función para realizar la eliminación del libro seleccionado
    def realizar_eliminacion():
        titulo_seleccionado = libro_seleccionado.get()

        for libro in biblioteca.libros:
            if libro.titulo == titulo_seleccionado:
                biblioteca.libros.remove(libro)
                biblioteca.guardar_csv()  # Actualizar el archivo CSV sin el libro eliminado
                messagebox.showinfo("Éxito", f"El libro '{titulo_seleccionado}' se ha eliminado correctamente.")
                ventana_eliminar.destroy()
                ventana_biblioteca.deiconify()  # Mostrar la ventana de biblioteca existente
                return

        messagebox.showerror("Error", f"No se encontró el libro '{titulo_seleccionado}' para eliminar.")

    # Botón para realizar la eliminación
    eliminar_button = tk.Button(ventana_eliminar, text="Eliminar Libro", command=realizar_eliminacion, cursor="hand2",
                                relief="flat", bg=fondo_correcto, font=("Comic Sans MS", 14, "bold"),
                                activebackground="red")
    eliminar_button.pack(pady=10)

    # Botón para regresar a la ventana principal de Biblioteca
    def regresar():
        ventana_eliminar.destroy()
        ventana_biblioteca.deiconify()  # Mostrar la ventana de biblioteca existente

    regresar_button = tk.Button(ventana_eliminar, text="Regresar", command=regresar, cursor="hand2", relief="flat",
                                bg=fondo_correcto, font=("Comic Sans MS", 14, "bold"), activebackground="red")
    regresar_button.pack(pady=10)

    ventana_eliminar.mainloop()

# Crear una instancia de la biblioteca
biblioteca = Biblioteca()

def incorrecta():
    ventana.withdraw()
    root = tk.Toplevel()
    root.title("Error")
    root.geometry("500x500+500+50")
    root.resizable(width=False, height=False)
    fondo = tk.PhotoImage(file="error.png")
    fondo1 = tk.Label(root, image=fondo)
    fondo1.place(x=0, y=0, relwidth=1, relheight=1)

    def regreso():
        root.withdraw()
        ventana.deiconify()

    boton4 = tk.Button(root, text="Regresar", command=regreso, cursor="hand2", relief="flat", bg=fondo_incorrecto,font=("Comic Sans MS", 20, "bold"))
    boton4.place(x=183, y=388)
    root.mainloop()

def salir():
    ventana.destroy()

# Ventana
ventana = Tk()
ventana.title("Login")
ventana.geometry("500x500+500+50")
ventana.resizable(width=False, height=False)
fondo = tk.PhotoImage(file="Entrada.png")
fondo1 = tk.Label(ventana, image=fondo)
fondo1.place(x=0, y=0, relwidth=1, relheight=1)

usuario = tk.StringVar()
password = tk.StringVar()

# Entradas
entrada = tk.Entry(ventana, textvar=usuario, width=20, relief="flat", bg=fondo_entrada, font=("Comic Sans MS", 14))
entrada.place(x=210, y=200)
entrada2 = tk.Entry(ventana, textvar=password, show="*", width=16, relief="flat", bg=fondo_entrada,
                    font=("Comic Sans MS", 14, "bold"))
entrada2.place(x=270, y=265, height=25)

# Botones
boton = tk.Button(ventana, text="Entrar", cursor="hand2", command=login, bg=fondo_entrar, width=11, relief="flat",
                  font=("Comic Sans MS", 17, "bold"))
boton.place(x=51, y=365)
boton1 = tk.Button(ventana, text="Salir", command=salir, cursor="hand2", bg=fondo_salir, width=11, relief="flat",
                   font=("Comic Sans MS", 17, "bold"))
boton1.place(x=280, y=365)


ventana.mainloop()
