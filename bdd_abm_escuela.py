import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.simpledialog
import mysql.connector

conexion = mysql.connector.connect(host="localhost", user="root", password="123456", database="escuela")

def cargar_datos():
    tree.delete(*tree.get_children()) 
    cursor = conexion.cursor()
    # SELECT para que solo muestre los regulares y los activos 
    cursor.execute("SELECT Alumnos.IDALUMNO, Alumnos.NOMBRE, Alumnos.APELLIDO, Alumnos.DNI, Carreras.NOMBRE, EstadoAlumno.NOMBRE FROM Alumnos JOIN Carreras ON Alumnos.IDCARRERA = Carreras.IDCARRERA JOIN EstadoAlumno ON Alumnos.IDESTADOALUMNO = EstadoAlumno.IDESTADOALUMNO WHERE EstadoAlumno.NOMBRE = 'Regular' AND Alumnos.ESTADO = 'Activo'")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def guardar_alumno():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()
    carrera_nombre = carrera_combobox.get()
    estado_alumno_nombre =estado_alumno_combobox.get()  
    estado_alumno = None  

    # Validación del DNI
    if not dni.isdigit() or len(dni) != 8:
        messagebox.showerror("Error", "El DNI debe contener exactamente 8 números.")
        return

    if nombre and apellido and dni and carrera_nombre and estado_alumno_nombre:
        carrera_id = obtener_id_carrera(carrera_nombre)
        estado_alumno = obtener_id_estado(estado_alumno_nombre)

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Alumnos (NOMBRE, APELLIDO, DNI, IDCARRERA, IDESTADOALUMNO) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, dni, carrera_id, estado_alumno))
        conexion.commit()
        cargar_datos()  
        limpiar()
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos.")

# Función para limpiar la grilla 
def limpiar():
    nombre_entry.delete(0, tk.END)
    apellido_entry.delete(0, tk.END)
    dni_entry.delete(0, tk.END)
    carrera_combobox.set("")  
    estado_alumno_combobox.set("")  
    editar_button.config(state=tk.DISABLED) 

def cargar_carreras():
    cursor = conexion.cursor()
    cursor.execute("SELECT IDCARRERA, NOMBRE FROM Carreras ORDER BY NOMBRE")
    carreras = cursor.fetchall()
    carrera_combobox['values'] = [row[1] for row in carreras]
    return carreras  

def cargar_estados_alumno():
    cursor = conexion.cursor()
    cursor.execute("SELECT IDESTADOALUMNO, NOMBRE FROM EstadoAlumno ORDER BY NOMBRE")
    estados = cursor.fetchall()
    estado_alumno_combobox['values'] = [row[1] for row in estados]
    return estados  

def nombre_carrera(id_carrera):
    for carrera in carreras:
        if carrera[0] == id_carrera:
            return carrera[1]
    return ""

def nombre_estado(id_estado):
    for estado in estados:
        if estado[0] == id_estado:
            return estado[1]
    return ""

def obtener_id_estado(nombre_estado):
    for estado in estados:
        if estado[1] == nombre_estado:
            return estado[0]
    return None

def obtener_id_carrera(nombre_carrera):
    for carrera in carreras:
        if carrera[1] == nombre_carrera:
            return carrera[0]
    return None

def mostrar_alerta(mensaje):
    messagebox.showwarning("Alerta", mensaje)

def editar_alumno (event):
    seleccion = tree.selection()
    if not seleccion:
        return  
    
    item = tree.item(seleccion)
    id_alumno = item['values'][0] 

    cursor = conexion.cursor()
    cursor.execute("SELECT NOMBRE, APELLIDO, DNI, IDCARRERA, IDESTADOALUMNO FROM Alumnos WHERE IDALUMNO = %s", (id_alumno,))
    alumno = cursor.fetchone()

    nombre_entry.delete(0, tk.END)
    nombre_entry.insert(0, alumno[0])
    apellido_entry.delete(0, tk.END)
    apellido_entry.insert(0, alumno[1])
    dni_entry.delete(0, tk.END)
    dni_entry.insert(0, alumno[2])

    carrera_nombre = nombre_carrera(alumno[3])
    estado_alumno_nombre = nombre_estado(alumno[4])

    carrera_combobox.set(carrera_nombre) 
    estado_alumno_combobox.set(estado_alumno_nombre)
    
    # Habilitar el botón de "Editar"
    editar_button.config(state=tk.NORMAL)
    global id_alumno_seleccionado
    id_alumno_seleccionado = id_alumno

def guardar_cambios():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()
    carrera_nombre = carrera_combobox.get()
    estado_alumno_nombre = estado_alumno_combobox.get()  
    estado_alumno = None  
    
    # Validacion de DNI
    if not dni.isdigit() or len(dni) != 8:
        messagebox.showerror("Error", "El DNI debe contener exactamente 8 números.")
        return

    if nombre and apellido and dni and carrera_nombre and estado_alumno_nombre:
        carrera_id = obtener_id_carrera(carrera_nombre)
        estado_alumno = obtener_id_estado(estado_alumno_nombre)

        cursor = conexion.cursor()
        
        # Actualizar en base de datos la información
        cursor.execute("UPDATE Alumnos SET NOMBRE = %s, APELLIDO = %s, DNI = %s, IDCARRERA = %s, IDESTADOALUMNO = %s WHERE IDALUMNO = %s", (nombre, apellido, dni, carrera_id, estado_alumno, id_alumno_seleccionado))
        conexion.commit()
        cargar_datos() 
        mostrar_alerta("Cambios guardados exitosamente.")
        limpiar()
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos.")



#En la base de datos al final agregué una columna nueva en alumnos de "ACTIVO, INACTIVO"
def eliminar_alumno():
    seleccion = tree.selection()
    if not seleccion:
        return
    
    item = tree.item(seleccion)
    id_alumno = item['values'][0]

    # Obtener el nombre del alumno
    nombre_alumno = item['values'][1]  # Suponiendo que el nombre del alumno se encuentra en la segunda columna
    
    # Preguntar al usuario si realmente desea eliminar el alumno
    while True:
        confirmacion = tkinter.simpledialog.askstring("Confirmar eliminación", f"¿Estás seguro de eliminar al alumno {nombre_alumno}? (Sí/No)")
        
        if confirmacion and confirmacion.lower() == "si":
            cursor = conexion.cursor()
            cursor.execute("UPDATE Alumnos SET ESTADO = 'Inactivo' WHERE IDALUMNO = %s", (id_alumno,))
            conexion.commit()
            cargar_datos()
            mostrar_alerta(f"Alumno {nombre_alumno} eliminado correctamente.")
            break
        elif confirmacion and confirmacion.lower() == "no":
            break

# Definición Grafica 
root = tk.Tk()
root.title("Consulta de Alumnos")

formulario_frame = tk.Frame(root, bd=2, relief=tk.SOLID, bg="light steel blue" )
formulario_frame.pack(padx=10, pady=10)

titulo_label = tk.Label(formulario_frame, text="Formulario Inscripción", font=("Helvetica", 14, "bold"), bg="light steel blue")
titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

nombre_label = tk.Label(formulario_frame, text="Nombre:", bg="light steel blue")
nombre_label.grid(row=1, column=0)
nombre_entry = tk.Entry(formulario_frame, width=20, bd=5,insertwidth=1,justify="center" )
nombre_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

apellido_label = tk.Label(formulario_frame, text="Apellido:", bg="light steel blue")
apellido_label.grid(row=2, column=0)
apellido_entry = tk.Entry(formulario_frame, width=20, bd=5,insertwidth=1,justify="center")
apellido_entry.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

dni_label = tk.Label(formulario_frame, text="DNI:", bg="light steel blue")
dni_label.grid(row=3, column=0)
dni_entry = tk.Entry(formulario_frame, width=20, bd=5,insertwidth=1,justify="center")
dni_entry.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

carrera_label = tk.Label(formulario_frame, text="Carrera:", bg="light steel blue")
carrera_label.grid(row=4, column=0)
carrera_combobox = ttk.Combobox(formulario_frame, state="readonly", width=20,justify="center")  
carrera_combobox.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

estado_label = tk.Label(formulario_frame, text="Estado del Alumno:", bg="light steel blue")
estado_label.grid(row=5, column=0)
estado_alumno_combobox = ttk.Combobox(formulario_frame, state="readonly", width=20, justify= "center")  
estado_alumno_combobox.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

carreras = cargar_carreras()
estados = cargar_estados_alumno()

guardar_button = tk.Button(formulario_frame, text="Guardar", command=guardar_alumno, bg="dark turquoise", fg="black", font=("poppins", 10, "bold"))
guardar_button.grid(row=6, columnspan=2, pady=10, sticky="ew")

cargar_button = tk.Button(formulario_frame, text="Cargar Datos", command=cargar_datos, bg="dark turquoise", fg="black", font=("poppins", 10, "bold"))
cargar_button.grid (row=7, columnspan= 2, pady= 10, sticky= "ew" )


tree = ttk.Treeview(root, columns=("ID", "Nombre", "Apellido", "DNI", "Carrera", "Estado"))
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Apellido")
tree.heading("#4", text="DNI")
tree.heading("#5", text="Carrera")
tree.heading("#6", text="Estado")
tree.column("#1", width=0, stretch=tk.NO)  
tree.column("#0", width=0, stretch=tk.NO)  
tree.pack(padx=10, pady=10)

tree.bind("<ButtonRelease-1>", editar_alumno)

editar_button = tk.Button(root, text="Editar", command=guardar_cambios, state=tk.DISABLED, bg="medium spring green", fg="black", font=("poppins", 10, "bold"))
editar_button.pack (pady=5)

eliminar_button = tk.Button(root, text="Eliminar", command=eliminar_alumno, bg="red", fg="white",font=("poppins", 10, "bold") )
eliminar_button.pack(pady=5)

root.mainloop()

conexion.close()