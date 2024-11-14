import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from backend import convertir_a_dzn, leer_dzn, ejecutar_dzn

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MinPol")
        self.dzn_file = None
        
    def run(self):
        self.create_main_window()
        self.root.mainloop()
        
    def create_main_window(self, width=700, height=600):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        tk.Label(self.root).pack(pady=50)
        
        image_path3 = "img/main.png"
        imagemain = Image.open(image_path3)
        imagemain = imagemain.resize((200, 200), Image.Resampling.LANCZOS) 
        main_img = ImageTk.PhotoImage(imagemain)
        img_label = tk.Label(self.root, image=main_img)
        img_label.image = main_img
        img_label.pack(pady=1)
        tk.Label(self.root, text="Minimizar la Polarización presenten en una Población", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Iniciar programa", command=self.create_second_window, font=("Arial", 12)).pack(pady=10)

    def create_second_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Seleccion de Programa")
        width=700
        height=600 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        new_window.geometry(f"{width}x{height}+{x}+{y}")
        new_window.resizable(False, False)
        
        self.opciones_canvas = tk.Canvas(new_window)
        self.opciones_canvas.grid(row=0, column=0, padx=110, pady=100, sticky="ns")
        
        tk.Label(self.opciones_canvas, text="to dzn",font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.opciones_canvas, text="MinPol",font=("Arial", 16)).grid(row=2, column=1, padx=10, pady=5)
        
        image_path2 = "img/convert.png"
        image2 = Image.open(image_path2)
        image2 = image2.resize((200, 200), Image.Resampling.LANCZOS) 
        convert_img = ImageTk.PhotoImage(image2)
        convert_label = tk.Label(self.opciones_canvas, image=convert_img)
        convert_label.image = convert_img
        convert_label.grid(row=3, column=0, padx=25, pady=5)
        
        image_path = "img/people.png"
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.Resampling.LANCZOS) 
        people_img = ImageTk.PhotoImage(image)
        people_label = tk.Label(self.opciones_canvas, image=people_img)
        people_label.image = people_img
        people_label.grid(row=3, column=1, padx=25, pady=5)
        
        tk.Button(self.opciones_canvas, text="Convertir",font=("Arial", 12), command=self.convertir_archivo).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(self.opciones_canvas, text="Ejecutar",font=("Arial", 12), command=self.variables_iniciales).grid(row=4, column=1, padx=10, pady=5)
        
    def minpol_window(self):
        new_window2 = tk.Toplevel(self.root)
        new_window2.title("MinPol")
        new_window2.state('zoomed')
        new_window2.rowconfigure(0, weight=1)
        
        self.varin_canva = tk.Canvas(new_window2)
        self.varin_canva.grid(row=0,column=0, padx=10, pady=5, sticky="ns")
        
        tk.Label(self.varin_canva, text="Polarización Inicial de la Poblacion",
                 font=("Arial", 14),
                 anchor="center").grid(row=0,column=0,pady=5,columnspan=2)
        
        tk.Label(self.varin_canva, text="N° Personas:",
                 font=("Arial", 10),
                 anchor="center").grid(row=1,column=0,pady=5)
        self.personas_label = tk.Label(self.varin_canva, text="", font=("Arial", 14))
        self.personas_label.grid(row=1,column=1,padx=10,pady=5)
        
        tk.Label(self.varin_canva, text="Posibles Opiniones:",
                 font=("Arial", 10),
                 anchor="center").grid(row=2,column=0,pady=5)
        self.opiniones_label = tk.Label(self.varin_canva, text="", font=("Arial", 14))
        self.opiniones_label.grid(row=2,column=1,padx=10,pady=5)
        
        tk.Label(self.varin_canva, text="Costo Maximo Permitido:",
                 font=("Arial", 10),
                 anchor="center").grid(row=3,column=0,pady=5)
        self.costo_maximo_label = tk.Label(self.varin_canva, text="", font=("Arial", 14))
        self.costo_maximo_label.grid(row=3,column=1,padx=10,pady=5)
        
        tk.Label(self.varin_canva, text="Numero Max movimientos:",
                 font=("Arial", 10),
                 anchor="center").grid(row=4,column=0,pady=5)
        self.max_mov_label = tk.Label(self.varin_canva, text="", font=("Arial", 14))
        self.max_mov_label.grid(row=4,column=1,padx=10,pady=5)
        
        self.separator = tk.Canvas(new_window2, bg="#111112",width=5)
        self.separator.grid(row=0,column=2, padx=10, pady=5, sticky="ns")
        
        # Canva para mostrar los resultados
        self.result_canva = tk.Canvas(new_window2)
        self.result_canva.grid(row=0,column=3, padx=10, pady=5, sticky="ns")
        
        tk.Label(self.result_canva, text="Polarización Minima de la poblacion",
                 font=("Arial", 14),
                 anchor="center").grid(row=0,column=0,pady=5,columnspan=2)
        
        tk.Label(self.result_canva, text="Costo total de la solucion:",
                 font=("Arial", 10),
                 anchor="center").grid(row=1,column=0,pady=5)
        self.costo_label = tk.Label( self.result_canva, text="", font=("Arial", 14))
        self.costo_label.grid(row=1,column=1,padx=10,pady=5)
        
        tk.Label(self.result_canva, text="Movimientos realizados:",
                 font=("Arial", 10),
                 anchor="center").grid(row=2,column=0,pady=5)
        self.mov_label = tk.Label( self.result_canva, text="", font=("Arial", 14))
        self.mov_label.grid(row=2,column=1,padx=10,pady=5)
        
        tk.Label( self.result_canva, text="Polarizacion Minima Alcanzada:",
                 font=("Arial", 10),
                 anchor="center").grid(row=3,column=0,pady=5)
        self.minpol_label = tk.Label( self.result_canva, text="", font=("Arial", 14))
        self.minpol_label.grid(row=3,column=1,padx=10,pady=5)
        
        tk.Button(self.result_canva, text="Ejecutar Modelo",
                  font=("Arial", 12),
                  anchor="center", 
                  command=self.resultados_modelo).grid(row=4,column=0,padx=10,pady=10,columnspan=2)
        
    def convertir_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Text Files", "*.mpl")])
        if archivo:
            try:
                archivo_dzn = convertir_a_dzn(archivo)
                messagebox.showinfo("Éxito", f"Archivo convertido y guardado como {archivo_dzn}")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema: {e}")
    
    def variables_iniciales(self):
    # Cuadro de diálogo para seleccionar el archivo .dzn
        ruta_archivo_dzn = filedialog.askopenfilename(filetypes=[("DZN Files", "*.dzn")])

        # Almacenamos la ruta del archivo .dzn
        self.dzn_file = ruta_archivo_dzn
        
        if ruta_archivo_dzn:
            try:
                datos = leer_dzn(ruta_archivo_dzn)
                
                # Mostrar datos en etiquetas como ejemplo
                self.minpol_window()
                self.personas_label.config(text=datos['n']) 
                self.opiniones_label.config(text=datos['m'])
                self.costo_maximo_label.config(text=datos['ct'])
                self.max_mov_label.config(text=datos['MaxMovs'])
                self.crear_histograma(datos['m'], datos['p'])
                # print(datos['m'], datos['p'])

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo .dzn: {e}")
        else:
            messagebox.showinfo("Info", "No se seleccionó ningún archivo")
    
    def crear_histograma(self, m, p):
        fig, ax = plt.subplots(figsize=(6, 4.5))
        colores = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(m)]
        bars = ax.bar(range(1, m + 1), p, color=colores, edgecolor="black")
        ax.bar(range(1, m + 1), p, color=colores, edgecolor="black")
        ax.set_xlabel("Opiniones")
        ax.set_ylabel("Número de Personas")
        ax.set_title("Distribución de Personas por Opinión")
        ax.set_xticks(range(1, m + 1))  # Etiquetas de 1 a m en el eje x

        # Agregar el valor exacto en la parte superior de cada barra
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')
    
        canvas = FigureCanvasTkAgg(fig, master=self.varin_canva)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5,column=0,padx=20,pady=25,columnspan=2)
        
    def resultados_modelo(self):
        resultados = ejecutar_dzn(self.dzn_file)

        self.costo_label.config(text=resultados['costo_total']) 
        self.mov_label.config(text=resultados['total_pasos_realizados'])
        self.minpol_label.config(text=resultados['polarizacion'])
        distribucion_final = resultados['distribucion_final']
        self.crear_histograma_modelo(len(distribucion_final), distribucion_final)
        
    def crear_histograma_modelo(self, m, p):
        fig, ax = plt.subplots(figsize=(6, 4.5))
        colores = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(m)]
        bars = ax.bar(range(1, m + 1), p, color=colores, edgecolor="black")
        ax.bar(range(1, m + 1), p, color=colores, edgecolor="black")
        ax.set_xlabel("Opiniones")
        ax.set_ylabel("Número de Personas")
        ax.set_title("Distribución de Personas por Opinión")
        ax.set_xticks(range(1, m + 1))  # Etiquetas de 1 a m en el eje x

        # Agregar el valor exacto en la parte superior de cada barra
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=self.result_canva)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5,column=0,padx=20,pady=25,columnspan=2)
