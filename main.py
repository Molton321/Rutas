import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import pickle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from Clases.aeropuerto import Aeropuerto
from Clases.ruta import Ruta
from tkinter import messagebox
from tkinter import font

# Crear una ventana de Tkinter
root = tk.Tk()
root.title("Rutas")
root.config(width=1200, height=700)
root.geometry("1086x670")
root.iconbitmap("./mapa.ico")

fuente_personalizada = font.Font(family="Verdana", size=10)
estilo = ttk.Style()
estilo.configure("Button", font=fuente_personalizada)
estilo.configure("Treeview", font=fuente_personalizada)
root.option_add("*Toplevel*Font", fuente_personalizada)

# Cambiar la fuente de todos los widgets Label
root.option_add("*Label*Font", fuente_personalizada)

# Cambiar la fuente de todos los widgets Button
root.option_add("*Button*Font", fuente_personalizada)

root.option_add("*heading*Font", fuente_personalizada)

root.option_add("Entry*Font", fuente_personalizada)


frame_dinamico = tk.Frame(root, bg="white")
frame_dinamico.pack(fill="both", expand=True, padx=50)

tabla = None
codigo_aeropuerto = None
codigo_ruta = None
nombre = None
ubicacion = None
origen = None
destino = None
distancia = None
tiempo = None

aeropuertos_dict = {}
rutas_dict = {}

def center_window(root, width=1086, height=670):
    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular la posición central
    center_x = (screen_width // 2) - (width // 2)
    center_y = (screen_height // 2) - (height // 2)

    # Posicionar la ventana en el centro de la pantalla
    root.geometry(f'{width}x{height}+{center_x}+{center_y}')

#Funciones
def frame_crear_aeropuerto(event=None):
    global codigo_aeropuerto, nombre, ubicacion
    
    for widget in frame_dinamico.winfo_children():
        widget.destroy()

    label_codigo = tk.Label(frame_dinamico, text="Ingrese el código:")
    codigo_aeropuerto = tk.Entry(frame_dinamico)
    
    label_nombre = tk.Label(frame_dinamico, text="Ingrese el nombre:")
    nombre = tk.Entry(frame_dinamico)
    
    label_ubicacion = tk.Label(frame_dinamico, text="Ingrese la ubicación:")
    ubicacion = tk.Entry(frame_dinamico)
    
    # Posicionar los labels y entries
    label_codigo.grid(row=0, column=0, pady=15)
    codigo_aeropuerto.grid(row=0, column=1)

    label_nombre.grid(row=1, column=0, pady=15)
    nombre.grid(row=1, column=1)

    label_ubicacion.grid(row=2, column=0, pady=15)
    ubicacion.grid(row=2, column=1)
    
    boton_crear_aeropuerto = tk.Button(frame_dinamico, text="Crear Aeropuerto", command=lambda: crear_aeropuerto(codigo_aeropuerto.get(), nombre.get(), ubicacion.get()))
    boton_crear_aeropuerto.grid(row=3, column=0, padx=5, pady=2, ipadx=15)
    
    boton_actualizar_aeropuerto = tk.Button(frame_dinamico, text="Actualizar Aeropuerto", command=lambda: actualizar_aeropuerto(codigo_aeropuerto.get(), nombre.get(), ubicacion.get()))
    boton_actualizar_aeropuerto.grid(row=3, column=1, padx=5, pady=2, ipadx=15)
    
    boton_eliminar_aeropuerto = tk.Button(frame_dinamico, text="Eliminar Aeropuerto", command=lambda: eliminar_aeropuerto(codigo_aeropuerto.get()))
    boton_eliminar_aeropuerto.grid(row=3, column=2, padx=5, pady=2, ipadx=15)
    
    
    actualizar_tabla()

def actualizar_tabla():
    
    global tabla, aeropuertos_dict
    aeropuertos = []
    
    with open("aeropuertos.pkl", "rb") as f:
        aeropuertos = pickle.load(f)
    
    tabla = ttk.Treeview(frame_dinamico)

    # Definir las columnas
    tabla['columns'] = ('#1', '#2', '#3')

    # Ocultar la columna de identificación
    tabla.column('#0', width=0, stretch='no')

    # Configurar las columnas
    tabla.column('#1', anchor='center', width=300)
    tabla.column('#2', anchor='center', width=300)
    tabla.column('#3', anchor='center', width=300)
    tabla.heading('#1', text='Nombre', anchor='center')
    tabla.heading('#2', text='Código', anchor='center')
    tabla.heading('#3', text='Ubicación', anchor='center')
    
    # Crear un diccionario para almacenar los objetos aeropuerto
    global aeropuertos_dict

    # Insertar datos en la tabla
    for aeropuerto in aeropuertos:
        item_id = tabla.insert('', 'end', values=(aeropuerto.get_nombre(), aeropuerto.get_codigo(), aeropuerto.get_ubicacion()))
        aeropuertos_dict[item_id] = aeropuerto
        
    # Asignar la función doble_click al evento de doble clic
    tabla.bind('<Double-1>', doble_click_aeropuerto)
    
    tabla.grid(row=4, column=0, columnspan=3, pady=2, padx=15)
    
    
def actualizar_tabla_rutas():
    
    global tabla, rutas_dict
    rutas = []
    
    with open("rutas.pkl", "rb") as f:
        rutas = pickle.load(f)
    
    tabla = ttk.Treeview(frame_dinamico)

    # Definir las columnas
    tabla['columns'] = ('#1', '#2', '#3', '#4', '#5')


    # Ocultar la columna de identificación
    tabla.column('#0', width=0, stretch='no')

    # Configurar las columnas
    tabla.column('#1', anchor='center', width=200)
    tabla.column('#2', anchor='center', width=200)
    tabla.column('#3', anchor='center', width=200)
    tabla.column('#4', anchor='center', width=200)
    tabla.column('#5', anchor='center', width=200)
    tabla.heading('#1', text='Codigo', anchor='center')
    tabla.heading('#2', text='Origen', anchor='center')
    tabla.heading('#3', text='Destino', anchor='center')
    tabla.heading('#4', text='Distancia', anchor='center')
    tabla.heading('#5', text='Tiempo', anchor='center')
    
    # Insertar datos en la tabla
    for ruta in rutas:
        item_id = tabla.insert('', 'end', values=(ruta.get_codigo(), ruta.get_origen(), ruta.get_destino(), ruta.get_distancia(), ruta.get_tiempo()))
        rutas_dict[item_id] = ruta
        
    # Asignar la función doble_click al evento de doble clic
    tabla.bind('<Double-1>', doble_click_ruta)
    
    tabla.grid(row=6, column=0, columnspan=3, pady=2)


def doble_click_ruta(event):
    
    global tabla, codigo_ruta, aeropuertos_dict, origen, destino, distancia, tiempo
    # Obtener el item seleccionado
    item = tabla.selection()[0]
    # Obtener el aeropuerto correspondiente al item seleccionado
    ruta = rutas_dict[item]
    # Obtener los datos del aeropuerto
    codigo_text = ruta.get_codigo()
    origen_text = ruta.get_origen()
    destino_text = ruta.get_destino()
    distancia_text = ruta.get_distancia()
    tiempo_text = ruta.get_tiempo()
        
    # Actualizar los entries con los datos del aeropuerto
    if codigo_ruta is not None:
        codigo_ruta.delete(0, tk.END)
        codigo_ruta.insert(0, codigo_text)
    if origen is not None:
        origen.delete(0, tk.END)
        origen.set(origen_text)
    if destino is not None:
        destino.delete(0, tk.END)
        destino.set(destino_text)
    if distancia is not None:
        distancia.delete(0, tk.END)
        distancia.insert(0, distancia_text)
    if tiempo is not None:
        tiempo.delete(0, tk.END)
        tiempo.insert(0, tiempo_text)
    
def crear_aeropuerto(codigo, nombre, ubicacion):
    
    if confirmar_contenido_aeropuerto(codigo, nombre, ubicacion) == False:
        
    
        aeropuertos = []
        
        with open("aeropuertos.pkl", "rb") as f:
            aeropuertos = pickle.load(f)
        
        existe = False
        
        for aeropuerto in aeropuertos:
            if aeropuerto.get_codigo() == codigo:
                existe = True
                break
        
        if existe:
            messagebox.showerror(message="El aeropuerto ya existe.", title="Advertencia")
        
        else:
            
            nuevo_aeropuerto = Aeropuerto(nombre, ubicacion, codigo)
            
            aeropuertos.append(nuevo_aeropuerto)
            
            with open('aeropuertos.pkl', 'wb') as f:
                pickle.dump(aeropuertos, f)
            
            limpiar_frame_aeropuerto()
            actualizar_tabla()

   
def actualizar_aeropuerto(codigo, nombre, ubicacion):
    
    if confirmar_contenido_aeropuerto(codigo, nombre, ubicacion) == False:
        with open("aeropuertos.pkl", "rb") as f:
            lista_recuperada = pickle.load(f)
        
        viejo = ''
            
        for i in lista_recuperada:
            if i.get_codigo() == codigo:
                viejo = i.get_nombre()
                
                i.set_nombre(nombre)
                i.set_ubicacion(ubicacion)
                break
        
        # Guardar la lista actualizada en el archivo pickle
        with open("aeropuertos.pkl", "wb") as f:
            pickle.dump(lista_recuperada, f)
            
        actualizar_rutas(viejo, nombre)    
        limpiar_frame_aeropuerto()
        actualizar_tabla()

def confirmar_contenido_aeropuerto(codigo, nombre, ubicacion):
    respuesta = False
    
    if codigo == '':
        messagebox.showwarning(message="El código es obligatorio", title="Advertencia")
        respuesta = True
        
    if nombre == '':
        messagebox.showwarning(message="El nombre es obligatorio", title="Advertencia")
        respuesta = True
        
    if ubicacion == '':
        messagebox.showwarning(message="La ubicación es obligatoria", title="Advertencia")
        respuesta = True
        
    return respuesta
    
def eliminar_aeropuerto(codigo):
    
    if codigo != '':
        existe_ruta = False
        
        with open("aeropuertos.pkl", "rb") as f:
            aeropuertos = pickle.load(f)
        
        nombre_aeropuerto = ''
            
        for aeropuerto in aeropuertos:
            if aeropuerto.get_codigo() == codigo:
                nombre_aeropuerto = aeropuerto.get_nombre()
                break
        
        with open("rutas.pkl", "rb") as f:
            rutas = pickle.load(f)
        
        for ruta in rutas:
            if ruta.get_origen() == nombre_aeropuerto or ruta.get_destino() == nombre_aeropuerto:
                existe_ruta = True
                messagebox.showwarning(message="No puede ser eliminado.", title="Advertencia")
                break
        
        respuesta = messagebox.askyesno(message="¿Está seguro que desea eliminar el aeropuerto?.", title="Advertencia")
        
        if not existe_ruta and respuesta:
            aeropuertos = [a for a in aeropuertos if a.get_codigo() != codigo]
            with open("aeropuertos.pkl", "wb") as f:
                pickle.dump(aeropuertos, f)
        
        limpiar_frame_aeropuerto()
        actualizar_tabla()
    else:
        messagebox.showwarning(message="Debe ingresar el codigo del aeropuerto.", title="Advertencia")
    
def actualizar_rutas(nombre_viejo, nombre_nuevo):
    
    with open("rutas.pkl", "rb") as f:
        lista_recuperada = pickle.load(f)
    
    for i in lista_recuperada:
        if i.get_destino() == nombre_viejo:
            i.set_destino(nombre_nuevo)
            
    for i in lista_recuperada:
        if i.get_origen() == nombre_viejo:
            i.set_origen(nombre_nuevo)
               
    # Guardar la lista actualizada en el archivo pickle
    with open("rutas.pkl", "wb") as f:
        pickle.dump(lista_recuperada, f)
    
    # Recargar las rutas desde el archivo
    with open("rutas.pkl", "rb") as f:
        lista_recuperada = pickle.load(f)

    
def frame_crear_ruta(event=None):
    global codigo_ruta, origen, destino, distancia, tiempo
    
    for widget in frame_dinamico.winfo_children():
        widget.destroy()
     
    aeropuertos = []
    
    with open("aeropuertos.pkl", "rb") as f:
        lista_recuperada = pickle.load(f)
    
    for a in lista_recuperada:
        aeropuertos.append(a.get_nombre())
    
    label_origen = tk.Label(frame_dinamico, text="Escoja el origen:")
    origen = ttk.Combobox(
        frame_dinamico,
        state="readonly",
        values=aeropuertos
    )
    
    label_destino = tk.Label(frame_dinamico, text="Escoja el destino:")
    destino = ttk.Combobox(
        frame_dinamico,
        state="readonly",
        values=aeropuertos
    )
    
    label_codigo = tk.Label(frame_dinamico, text="Ingrese el código:")
    codigo_ruta = tk.Entry(frame_dinamico)
    
    label_distancia = tk.Label(frame_dinamico, text="Ingrese la distancia:")
    distancia = tk.Entry(frame_dinamico)
    
    label_tiempo = tk.Label(frame_dinamico, text="Ingrese el tiempo:")
    tiempo = tk.Entry(frame_dinamico)
    
    label_codigo.grid(row=0, column=0, pady=15)
    codigo_ruta.grid(row=0, column=1)
    
    label_origen.grid(row=1, column=0, pady=15)
    origen.grid(row=1, column=1)
    
    label_destino.grid(row=2, column=0, pady=15)
    destino.grid(row=2, column=1)
    
    label_distancia.grid(row=3, column=0, padx=15)
    distancia.grid(row=3, column=1)
    
    label_tiempo.grid(row=4, column=0, pady=15)
    tiempo.grid(row=4, column=1)
    
    boton_crear_ruta = tk.Button(frame_dinamico, text="Crear Ruta", command=lambda: crear_ruta(codigo_ruta.get() ,origen.get(), destino.get(), distancia.get(), tiempo.get()))
    boton_crear_ruta.grid(row=5, column=0, padx=5, pady=2, ipadx=15)

    boton_actualizar_ruta = tk.Button(frame_dinamico, text="Actualizar Ruta", command=lambda: actualizar_ruta(codigo_ruta.get(), origen.get(), destino.get(), distancia.get(), tiempo.get()))
    boton_actualizar_ruta.grid(row=5, column=1, padx=5, pady=2, ipadx=15)
    
    boton_eliminar_ruta = tk.Button(frame_dinamico, text="Eliminar Ruta", command=lambda: eliminar_ruta(codigo_ruta.get()))
    boton_eliminar_ruta.grid(row=5, column=2, padx=5, pady=2, ipadx=15)

    actualizar_tabla_rutas()



def crear_ruta(codigo, origen, destino, distancia, tiempo):
    
    if confirmar_contenido_ruta(codigo, origen, destino, distancia, tiempo) == False:
        
        rutas = []
        
        with open("rutas.pkl", "rb") as f:
            rutas = pickle.load(f)
        
        nueva_ruta = Ruta(codigo, origen, destino, distancia, tiempo)
        
        rutas.append(nueva_ruta)
        
        with open('rutas.pkl', 'wb') as f:
            pickle.dump(rutas, f)
        
        limpiar_frame_rutas()
        actualizar_tabla_rutas()
    
    
def actualizar_ruta(codigo, origen, destino, distancia, tiempo):
    
    if confirmar_contenido_ruta(codigo, origen, destino, distancia, tiempo) == False:
        
    
        with open("rutas.pkl", "rb") as f:
            rutas = pickle.load(f)
        
        for ruta in rutas:
            if ruta.get_codigo() == codigo:
                ruta.set_origen(origen)
                ruta.set_destino(destino)
                ruta.set_distancia(distancia)
                ruta.set_tiempo(tiempo)
                
                break
        
        # Guardar la lista actualizada en el archivo pickle
        with open("rutas.pkl", "wb") as f:
            pickle.dump(rutas, f)
            
        with open("rutas.pkl", "rb") as f:
            rutas = pickle.load(f)
            
        limpiar_frame_rutas()
        actualizar_tabla_rutas()
        

def confirmar_contenido_ruta(codigo, origen, destino, distancia, tiempo):
    respuesta = False
    
    if codigo == '':
        messagebox.showwarning(message="El código es obligatorio", title="Advertencia")
        respuesta = True
        
    if origen == '':
        messagebox.showwarning(message="El origen es obligatorio", title="Advertencia")
        respuesta = True
        
    if destino == '':
        messagebox.showwarning(message="El destino es obligatorio", title="Advertencia")
        respuesta = True
    
    if distancia == '':
        messagebox.showwarning(message="La distancia es obligatoria", title="Advertencia")
        respuesta = True
    
    if tiempo == '':
        messagebox.showwarning(message="El tiempo es obligatorio", title="Advertencia")
        respuesta = True
        
    return respuesta


def eliminar_ruta(codigo):
    
    if codigo != '':
        
        with open("rutas.pkl", "rb") as f:
            rutas = pickle.load(f)

        respuesta = messagebox.askyesno(message="¿Está seguro que desea eliminar esta ruta?.", title="Advertencia")

        if respuesta:
            rutas = [a for a in rutas if a.get_codigo() != codigo]
            with open("rutas.pkl", "wb") as f:
                pickle.dump(rutas, f)
        
        limpiar_frame_rutas()
        actualizar_tabla_rutas()
        
    else:
        messagebox.showwarning(message="Debe ingresar el código de la ruta.", title="Advertencia")


def frame_mostrar_rutas(ruta_mas_corta): 
    for widget in frame_dinamico.winfo_children():
        widget.destroy()

    with open("aeropuertos.pkl", "rb") as f:
        aeropuertos = pickle.load(f)
    
    with open("rutas.pkl", "rb") as f:
        rutas = pickle.load(f)

    aer = []
    
    for a in aeropuertos:
        aer.append(a.get_nombre())
        
    # Crear una variable de control StringVar para cada Combobox
    origen_var = tk.StringVar()
    destino_var = tk.StringVar()
    
    # Crear dos Combobox para seleccionar el origen y el destino
    
    label_origen = tk.Label(frame_dinamico, text="Origen:")
    label_destino = tk.Label(frame_dinamico, text="Destino:")
    
    origen = ttk.Combobox(frame_dinamico, textvariable=origen_var, values=aer)
    destino = ttk.Combobox(frame_dinamico, textvariable=destino_var, values=aer)

    # Crear un botón para elegir el origen y el destino
    boton = tk.Button(frame_dinamico, text="Elegir origen y destino", command=lambda: elegir_origen_destino(origen_var, destino_var))

    # Colocar los Combobox y el botón en el marco dinámico
    label_origen.grid(row=0, column=0)
    origen.grid(row=0, column=1)
    
    label_destino.grid(row=0, column=2)
    destino.grid(row=0, column=3)
    boton.grid(row=0, column=4)
  
    lab = {aeropuerto.get_nombre(): aeropuerto.get_nombre() for aeropuerto in aeropuertos}
    
    # Crear un grafo
    G = nx.Graph()

    # Agregar un nodo por cada aeropuerto
    for aeropuerto in aeropuertos:
        G.add_node(aeropuerto.get_nombre())
            
    # Agregar una arista por cada ruta
    for ruta in rutas:
        origen = ruta.get_origen()
        destino = ruta.get_destino()
        G.add_edge(origen, destino, distancia=ruta.get_distancia(), tiempo=ruta.get_tiempo())
    
    # Crear una figura de Matplotlib
    fig, ax = plt.subplots()

    # Dibujar el grafo en la figura de Matplotlib
    #o podria usar nx.spectral_layout
    pos = nx.circular_layout(G)  # Posiciones de los nodos
    nx.draw(G, pos, labels = lab, ax=ax, edge_color='blue', width=2, node_size = 1500) 
    
    # Agregar etiquetas a las aristas
    edge_labels = nx.get_edge_attributes(G, 'tiempo')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    
    if ruta_mas_corta is not None:
        # Dibujar las aristas de la ruta más corta en un color diferente
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=ruta_mas_corta, edge_color='red', width=2)

    # Crear un canvas de Tkinter y dibujar la figura de Matplotlib en él
    canvas = FigureCanvasTkAgg(fig, master=frame_dinamico)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, columnspan=4, pady=2)
    

def elegir_origen_destino(origen_var, destino_var):
    origen = origen_var.get()
    destino = destino_var.get()

    print(f'origen: {origen}, destino: {destino}')
    
    with open("aeropuertos.pkl", "rb") as f:
        aeropuertos = pickle.load(f)
    
    with open("rutas.pkl", "rb") as f:
        rutas = pickle.load(f)
    
    # Crear un grafo dirigido
    G = nx.Graph()

    # Agregar un nodo por cada aeropuerto
    for aeropuerto in aeropuertos:
        G.add_node(aeropuerto.get_nombre())

    # Agregar una arista por cada ruta
    for ruta in rutas:
        origen_ruta = ruta.get_origen()
        destino_ruta = ruta.get_destino()
        tiempo = float(ruta.get_tiempo())
        G.add_edge(origen_ruta, destino_ruta, tiempo=tiempo)

    # Calcular el camino más corto desde el origen hasta el destino
    camino_mas_rapido = nx.dijkstra_path(G, origen, destino, weight='tiempo')

    # Crear una lista de aristas a partir de la lista de nodos
    aristas_ruta = [(camino_mas_rapido[n], camino_mas_rapido[n + 1]) for n in range(len(camino_mas_rapido) - 1)]
    
    frame_mostrar_rutas(aristas_ruta)
    print('El camino más rápido es:', camino_mas_rapido)
        

def doble_click_aeropuerto(event):
    global tabla, aeropuertos_dict, codigo_aeropuerto, nombre, ubicacion
    # Obtener el item seleccionado
    item = tabla.selection()[0]
    # Obtener el aeropuerto correspondiente al item seleccionado
    aeropuerto = aeropuertos_dict[item]
    # Obtener los datos del aeropuerto
    nombre_text = aeropuerto.get_nombre()
    codigo_text = aeropuerto.get_codigo()
    ubicacion_text = aeropuerto.get_ubicacion()
    
    # Actualizar los entries con los datos del aeropuerto
    if codigo_aeropuerto is not None:
        codigo_aeropuerto.delete(0, tk.END)
        codigo_aeropuerto.insert(0, codigo_text)
    if nombre is not None:
        nombre.delete(0, tk.END)
        nombre.insert(0, nombre_text)
    if ubicacion is not None:
        ubicacion.delete(0, tk.END)
        ubicacion.insert(0, ubicacion_text)

def limpiar_frame_aeropuerto():
    if codigo_aeropuerto is not None:
        codigo_aeropuerto.delete(0, tk.END)
    if nombre is not None:
        nombre.delete(0, tk.END)
    if ubicacion is not None:
        ubicacion.delete(0, tk.END)
    

def limpiar_frame_rutas():
    if codigo_ruta is not None:
        codigo_ruta.delete(0, tk.END)
    if origen is not None:
        origen.insert(0, tk.END)
    if destino is not None:
        destino.delete(0, tk.END)
    if distancia is not None:
        distancia.delete(0, tk.END)
    if tiempo is not None:
        tiempo.delete(0, tk.END)
#Menú
barra_menu = tk.Menu()
menu_aeropuerto = tk.Menu(barra_menu, tearoff=False)
menu_rutas = tk.Menu(barra_menu, tearoff=False)
mostrar_rutas = tk.Menu(barra_menu, tearoff=False)

menu_aeropuerto.add_command(
    label="Gestionar Aeropuertos",
    accelerator="Ctrl+N",
    command=frame_crear_aeropuerto
)

root.bind_all("<Control-n>", frame_crear_aeropuerto)

menu_rutas.add_command(
    label="Gestionar rutas",
    accelerator="Ctrl+M",
    command=frame_crear_ruta
)

root.bind_all("<Control-m>", frame_crear_aeropuerto)

ruta_mas_corta = None

mostrar_rutas.add_command(
    label="Mostrar rutas",
    command=lambda: frame_mostrar_rutas(ruta_mas_corta)
)

barra_menu.add_cascade(menu=menu_aeropuerto, label="Aeropuertos")
barra_menu.add_cascade(menu=menu_rutas, label="Rutas")
barra_menu.add_cascade(menu=mostrar_rutas, label="Mostrar rutas")


root.config(menu=barra_menu)

center_window(root)
# Iniciar el bucle principal de Tkinter
root.mainloop()

