import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class MaquinaTuring:
    def __init__(self, estados, alfabeto, alfabeto_cinta, transiciones, estado_inicial, estados_aceptacion, estados_rechazo):
        self.estados = estados
        self.alfabeto = alfabeto
        self.alfabeto_cinta = alfabeto_cinta
        self.transiciones = transiciones
        self.estado_actual = estado_inicial
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.estados_rechazo = estados_rechazo
        self.cinta = ['_']  # Símbolo blanco
        self.posicion_cabezal = 0
        self.contador_pasos = 0
        self.historial = []
        
    def inicializar_cinta(self, cadena_entrada):
        """Inicializar la cinta con la cadena de entrada"""
        self.cinta = list(cadena_entrada) + ['_']
        self.posicion_cabezal = 0
        self.estado_actual = self.estado_inicial
        self.contador_pasos = 0
        self.historial = []
        self._guardar_estado()
        
    def _guardar_estado(self):
        """Guardar el estado actual para visualización"""
        self.historial.append({
            'cinta': self.cinta.copy(),
            'posicion_cabezal': self.posicion_cabezal,
            'estado_actual': self.estado_actual,
            'paso': self.contador_pasos
        })
        
    def ejecutar_paso(self):
        """Ejecutar un paso de la Máquina de Turing"""
        if self.estado_actual in self.estados_aceptacion or self.estado_actual in self.estados_rechazo:
            return False
            
        simbolo_actual = self.cinta[self.posicion_cabezal] if self.posicion_cabezal < len(self.cinta) else '_'
        
        # Buscar transición
        clave_transicion = (self.estado_actual, simbolo_actual)
        if clave_transicion not in self.transiciones:
            return False
            
        siguiente_estado, escribir_simbolo, direccion = self.transiciones[clave_transicion]
        
        # Escribir símbolo
        if self.posicion_cabezal < len(self.cinta):
            self.cinta[self.posicion_cabezal] = escribir_simbolo
        else:
            self.cinta.append(escribir_simbolo)
            
        # Mover cabezal
        if direccion == 'R':
            self.posicion_cabezal += 1
            if self.posicion_cabezal >= len(self.cinta):
                self.cinta.append('_')
        elif direccion == 'L':
            self.posicion_cabezal = max(0, self.posicion_cabezal - 1)
            
        # Actualizar estado
        self.estado_actual = siguiente_estado
        self.contador_pasos += 1
        self._guardar_estado()
        
        return True
        
    def ejecutar_hasta_parar(self):
        """Ejecutar hasta que la máquina se detenga"""
        while self.ejecutar_paso():
            pass
            
    def obtener_estado_actual(self):
        """Obtener el estado actual de la máquina"""
        if self.estado_actual in self.estados_aceptacion:
            return "ACEPTADA"
        elif self.estado_actual in self.estados_rechazo:
            return "RECHAZADA"
        else:
            return "EJECUTANDO"
            
    def obtener_cadena_cinta(self):
        """Obtener la cinta como cadena con la posición del cabezal marcada"""
        cadena_cinta = ""
        for i, simbolo in enumerate(self.cinta):
            if i == self.posicion_cabezal:
                cadena_cinta += f"[{simbolo}]"
            else:
                cadena_cinta += f" {simbolo} "
        return cadena_cinta.strip()

def crear_maquina_regex(patron_regex):
    """Crear Máquina de Turing para un patrón de expresión regular específico"""
    maquinas = {
        "(a|b)*abb": crear_maquina_abb(),
        "0*1*": crear_maquina_01_estrella(),
        "(ab)*": crear_maquina_ab_estrella(),
        "1(01)*0": crear_maquina_1010(),
        "(a+b)*a(a+b)*": crear_maquina_contiene_a(),
        "a*b*c*": crear_maquina_abc_estrella(),
        "(00)*1(11)*": crear_maquina_00111(),
        "a(a|b)*b": crear_maquina_inicia_a_termina_b(),
        "(0|1)*00(0|1)*": crear_maquina_contiene_00(),
        "1*01*01*": crear_maquina_dos_ceros()
    }
    return maquinas.get(patron_regex, crear_maquina_abb())

def crear_maquina_abb():
    """MT para (a|b)*abb"""
    estados = {'q0', 'q1', 'q2', 'q3', 'aceptar', 'rechazar'}
    alfabeto = {'a', 'b'}
    alfabeto_cinta = {'a', 'b', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', 'a'): ('q1', 'X', 'R'),
        ('q0', 'b'): ('q0', 'X', 'R'),
        ('q0', '_'): ('rechazar', '_', 'R'),
        
        ('q1', 'a'): ('q1', 'X', 'R'),
        ('q1', 'b'): ('q2', 'X', 'R'),
        
        ('q2', 'a'): ('q1', 'X', 'R'),
        ('q2', 'b'): ('q3', 'X', 'R'),
        
        ('q3', 'a'): ('q1', 'X', 'R'),
        ('q3', 'b'): ('q0', 'X', 'R'),
        ('q3', '_'): ('aceptar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones, 
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_01_estrella():
    """MT para 0*1*"""
    estados = {'q0', 'q1', 'aceptar', 'rechazar'}
    alfabeto = {'0', '1'}
    alfabeto_cinta = {'0', '1', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', '0'): ('q0', 'X', 'R'),
        ('q0', '1'): ('q1', 'X', 'R'),
        ('q0', '_'): ('aceptar', '_', 'R'),
        
        ('q1', '1'): ('q1', 'X', 'R'),
        ('q1', '0'): ('rechazar', 'X', 'R'),
        ('q1', '_'): ('aceptar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_ab_estrella():
    """MT para (ab)*"""
    estados = {'q0', 'q1', 'aceptar', 'rechazar'}
    alfabeto = {'a', 'b'}
    alfabeto_cinta = {'a', 'b', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', 'a'): ('q1', 'X', 'R'),
        ('q0', '_'): ('aceptar', '_', 'R'),
        ('q0', 'b'): ('rechazar', 'X', 'R'),
        
        ('q1', 'b'): ('q0', 'X', 'R'),
        ('q1', 'a'): ('rechazar', 'X', 'R'),
        ('q1', '_'): ('rechazar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_1010():
    """MT para 1(01)*0"""
    estados = {'q0', 'q1', 'q2', 'aceptar', 'rechazar'}
    alfabeto = {'0', '1'}
    alfabeto_cinta = {'0', '1', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', '1'): ('q1', 'X', 'R'),
        ('q0', '0'): ('rechazar', 'X', 'R'),
        
        ('q1', '0'): ('q2', 'X', 'R'),
        ('q1', '1'): ('rechazar', 'X', 'R'),
        
        ('q2', '1'): ('q1', 'X', 'R'),
        ('q2', '0'): ('aceptar', 'X', 'R'),
        ('q2', '_'): ('rechazar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_contiene_a():
    """MT para (a+b)*a(a+b)* (contiene al menos una 'a')"""
    estados = {'q0', 'q1', 'aceptar', 'rechazar'}
    alfabeto = {'a', 'b'}
    alfabeto_cinta = {'a', 'b', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', 'a'): ('q1', 'X', 'R'),
        ('q0', 'b'): ('q0', 'X', 'R'),
        ('q0', '_'): ('rechazar', '_', 'R'),
        
        ('q1', 'a'): ('q1', 'X', 'R'),
        ('q1', 'b'): ('q1', 'X', 'R'),
        ('q1', '_'): ('aceptar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_abc_estrella():
    """MT para a*b*c*"""
    estados = {'q0', 'q1', 'q2', 'aceptar', 'rechazar'}
    alfabeto = {'a', 'b', 'c'}
    alfabeto_cinta = {'a', 'b', 'c', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', 'a'): ('q0', 'X', 'R'),
        ('q0', 'b'): ('q1', 'X', 'R'),
        ('q0', 'c'): ('q2', 'X', 'R'),
        ('q0', '_'): ('aceptar', '_', 'R'),
        
        ('q1', 'b'): ('q1', 'X', 'R'),
        ('q1', 'c'): ('q2', 'X', 'R'),
        ('q1', 'a'): ('rechazar', 'X', 'R'),
        ('q1', '_'): ('aceptar', '_', 'R'),
        
        ('q2', 'c'): ('q2', 'X', 'R'),
        ('q2', 'a'): ('rechazar', 'X', 'R'),
        ('q2', 'b'): ('rechazar', 'X', 'R'),
        ('q2', '_'): ('aceptar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_00111():
    """MT para (00)*1(11)*"""
    estados = {'q0', 'q1', 'q2', 'q3', 'aceptar', 'rechazar'}
    alfabeto = {'0', '1'}
    alfabeto_cinta = {'0', '1', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', '0'): ('q1', 'X', 'R'),
        ('q0', '1'): ('q2', 'X', 'R'),
        ('q0', '_'): ('rechazar', '_', 'R'),
        
        ('q1', '0'): ('q0', 'X', 'R'),
        ('q1', '1'): ('rechazar', 'X', 'R'),
        
        ('q2', '1'): ('q3', 'X', 'R'),
        ('q2', '0'): ('rechazar', 'X', 'R'),
        
        ('q3', '1'): ('q2', 'X', 'R'),
        ('q3', '0'): ('rechazar', 'X', 'R'),
        ('q3', '_'): ('aceptar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_inicia_a_termina_b():
    """MT para a(a|b)*b"""
    estados = {'q0', 'q1', 'verificar_ultimo', 'aceptar', 'rechazar'}
    alfabeto = {'a', 'b'}
    alfabeto_cinta = {'a', 'b', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', 'a'): ('q1', 'X', 'R'),
        ('q0', 'b'): ('rechazar', 'X', 'R'),
        
        ('q1', 'a'): ('q1', 'X', 'R'),
        ('q1', 'b'): ('q1', 'X', 'R'),
        ('q1', '_'): ('verificar_ultimo', '_', 'L'),
        
        ('verificar_ultimo', 'b'): ('aceptar', 'X', 'R'),
        ('verificar_ultimo', 'a'): ('rechazar', 'X', 'R'),
        ('verificar_ultimo', 'X'): ('verificar_ultimo', 'X', 'L'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_contiene_00():
    """MT para (0|1)*00(0|1)*"""
    estados = {'q0', 'q1', 'aceptar', 'rechazar'}
    alfabeto = {'0', '1'}
    alfabeto_cinta = {'0', '1', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', '0'): ('q1', 'X', 'R'),
        ('q0', '1'): ('q0', 'X', 'R'),
        ('q0', '_'): ('rechazar', '_', 'R'),
        
        ('q1', '0'): ('aceptar', 'X', 'R'),
        ('q1', '1'): ('q0', 'X', 'R'),
        ('q1', '_'): ('rechazar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

def crear_maquina_dos_ceros():
    """MT para 1*01*01*"""
    estados = {'q0', 'q1', 'q2', 'aceptar', 'rechazar'}
    alfabeto = {'0', '1'}
    alfabeto_cinta = {'0', '1', 'X', '_'}
    estado_inicial = 'q0'
    estados_aceptacion = {'aceptar'}
    estados_rechazo = {'rechazar'}
    
    transiciones = {
        ('q0', '1'): ('q0', 'X', 'R'),
        ('q0', '0'): ('q1', 'X', 'R'),
        ('q0', '_'): ('rechazar', '_', 'R'),
        
        ('q1', '1'): ('q1', 'X', 'R'),
        ('q1', '0'): ('q2', 'X', 'R'),
        ('q1', '_'): ('rechazar', '_', 'R'),
        
        ('q2', '1'): ('q2', 'X', 'R'),
        ('q2', '0'): ('rechazar', 'X', 'R'),
        ('q2', '_'): ('aceptar', '_', 'R'),
    }
    
    return MaquinaTuring(estados, alfabeto, alfabeto_cinta, transiciones,
                        estado_inicial, estados_aceptacion, estados_rechazo)

class InterfazMaquinaTuring:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing - Estilo Teams")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2D2D30')
        
        self.mt = None
        self.regex_actual = ""
        self.modo_auto = False
        self.velocidad = 500  # ms entre pasos
        
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        # Marco principal con estilo tipo Teams
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure('TFrame', background='#2D2D30')
        estilo.configure('TLabel', background='#2D2D30', foreground='white', font=('Segoe UI', 10))
        estilo.configure('TButton', font=('Segoe UI', 10), padding=6)
        estilo.configure('TCombobox', font=('Segoe UI', 10))
        estilo.configure('TEntry', font=('Segoe UI', 10))
        
        # Encabezado
        marco_encabezado = ttk.Frame(self.root)
        marco_encabezado.pack(fill='x', padx=20, pady=10)
        
        etiqueta_titulo = ttk.Label(marco_encabezado, text="🧠 Simulador de Máquina de Turing", 
                                   font=('Segoe UI', 16, 'bold'), foreground='#4FA6FF')
        etiqueta_titulo.pack(side='left')
        
        # Área de contenido principal
        marco_principal = ttk.Frame(self.root)
        marco_principal.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Panel izquierdo - Controles
        marco_izquierdo = ttk.Frame(marco_principal)
        marco_izquierdo.pack(side='left', fill='y', padx=(0, 10))
        
        # Selección de regex
        marco_regex = ttk.LabelFrame(marco_izquierdo, text="Expresiones Regulares", padding=10)
        marco_regex.pack(fill='x', pady=(0, 10))
        
        self.variable_regex = tk.StringVar()
        opciones_regex = [
            "(a|b)*abb",
            "0*1*", 
            "(ab)*",
            "1(01)*0",
            "(a+b)*a(a+b)*",
            "a*b*c*",
            "(00)*1(11)*",
            "a(a|b)*b",
            "(0|1)*00(0|1)*",
            "1*01*01*"
        ]
        
        self.combo_regex = ttk.Combobox(marco_regex, textvariable=self.variable_regex, 
                                       values=opciones_regex, state='readonly')
        self.combo_regex.set("(a|b)*abb")
        self.combo_regex.pack(fill='x', pady=5)
        self.combo_regex.bind('<<ComboboxSelected>>', self.cambio_regex)
        
        # Sección de entrada
        marco_entrada = ttk.LabelFrame(marco_izquierdo, text="Cadena de Entrada", padding=10)
        marco_entrada.pack(fill='x', pady=(0, 10))
        
        ttk.Label(marco_entrada, text="Ingrese la cadena:").pack(anchor='w')
        self.entrada_texto = ttk.Entry(marco_entrada, font=('Segoe UI', 11))
        self.entrada_texto.pack(fill='x', pady=5)
        self.entrada_texto.insert(0, "aabb")
        
        # Botones de control
        marco_controles = ttk.LabelFrame(marco_izquierdo, text="Controles", padding=10)
        marco_controles.pack(fill='x', pady=(0, 10))
        
        fila_botones1 = ttk.Frame(marco_controles)
        fila_botones1.pack(fill='x', pady=2)
        
        self.boton_cargar = ttk.Button(fila_botones1, text="Cargar Cadena", command=self.cargar_cadena)
        self.boton_cargar.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.boton_paso = ttk.Button(fila_botones1, text="Paso a Paso", command=self.ejecutar_paso)
        self.boton_paso.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        fila_botones2 = ttk.Frame(marco_controles)
        fila_botones2.pack(fill='x', pady=2)
        
        self.boton_ejecutar = ttk.Button(fila_botones2, text="Ejecutar Todo", command=self.ejecutar_automatico)
        self.boton_ejecutar.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.boton_reiniciar = ttk.Button(fila_botones2, text="Reiniciar", command=self.reiniciar_maquina)
        self.boton_reiniciar.pack(side='left', fill='x', expand=True)
        
        # Control de velocidad
        marco_velocidad = ttk.Frame(marco_controles)
        marco_velocidad.pack(fill='x', pady=5)
        
        ttk.Label(marco_velocidad, text="Velocidad:").pack(side='left')
        self.escala_velocidad = ttk.Scale(marco_velocidad, from_=50, to=1000, 
                                        orient='horizontal', command=self.cambio_velocidad)
        self.escala_velocidad.set(500)
        self.escala_velocidad.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # Mostrar estado
        marco_estado = ttk.LabelFrame(marco_izquierdo, text="Estado Actual", padding=10)
        marco_estado.pack(fill='x', pady=(0, 10))
        
        self.etiqueta_estado = ttk.Label(marco_estado, text="Listo para comenzar", 
                                       font=('Segoe UI', 11, 'bold'), foreground='#4FA6FF')
        self.etiqueta_estado.pack(anchor='w')
        
        self.etiqueta_pasos = ttk.Label(marco_estado, text="Pasos: 0")
        self.etiqueta_pasos.pack(anchor='w')
        
        self.etiqueta_estado_actual = ttk.Label(marco_estado, text="Estado: -")
        self.etiqueta_estado_actual.pack(anchor='w')
        
        # Panel derecho - Visualización de cinta
        marco_derecho = ttk.Frame(marco_principal)
        marco_derecho.pack(side='right', fill='both', expand=True)
        
        marco_cinta = ttk.LabelFrame(marco_derecho, text="Cinta de la Máquina de Turing", padding=15)
        marco_cinta.pack(fill='both', expand=True)
        
        self.lienzo_cinta = tk.Canvas(marco_cinta, bg='#1E1E1E', relief='sunken', 
                                     borderwidth=2, highlightthickness=0)
        self.lienzo_cinta.pack(fill='both', expand=True)
        
        # Panel de historial
        marco_historial = ttk.LabelFrame(marco_derecho, text="Historial de Ejecución", padding=10)
        marco_historial.pack(fill='x', pady=(10, 0))
        
        self.texto_historial = tk.Text(marco_historial, height=8, bg='#1E1E1E', fg='white', 
                                      font=('Consolas', 9), state='disabled')
        barra_desplazamiento = ttk.Scrollbar(marco_historial, orient='vertical', command=self.texto_historial.yview)
        self.texto_historial.configure(yscrollcommand=barra_desplazamiento.set)
        
        self.texto_historial.pack(side='left', fill='both', expand=True)
        barra_desplazamiento.pack(side='right', fill='y')
        
        # Inicializar con el primer regex
        self.cambio_regex()
        
    def cambio_regex(self, event=None):
        self.regex_actual = self.variable_regex.get()
        self.reiniciar_maquina()
        
    def cambio_velocidad(self, valor):
        self.velocidad = int(float(valor))
        
    def cargar_cadena(self):
        cadena_entrada = self.entrada_texto.get().strip()
        if not cadena_entrada:
            messagebox.showwarning("Advertencia", "Por favor ingrese una cadena")
            return
            
        self.mt = crear_maquina_regex(self.regex_actual)
        self.mt.inicializar_cinta(cadena_entrada)
        self.actualizar_pantalla()
        self.agregar_al_historial(f"Cargada cadena: '{cadena_entrada}' para regex: {self.regex_actual}")
        
    def ejecutar_paso(self):
        if not self.mt:
            messagebox.showwarning("Advertencia", "Primero cargue una cadena")
            return
            
        if self.mt.obtener_estado_actual() in ["ACEPTADA", "RECHAZADA"]:
            messagebox.showinfo("Información", f"La máquina ya terminó: {self.mt.obtener_estado_actual()}")
            return
            
        self.mt.ejecutar_paso()
        self.actualizar_pantalla()
        
    def ejecutar_automatico(self):
        if not self.mt:
            messagebox.showwarning("Advertencia", "Primero cargue una cadena")
            return
            
        def ejecutar_automaticamente():
            self.modo_auto = True
            self.boton_ejecutar.config(state='disabled')
            self.boton_paso.config(state='disabled')
            
            while (self.modo_auto and self.mt and 
                   self.mt.obtener_estado_actual() == "EJECUTANDO"):
                self.mt.ejecutar_paso()
                self.root.after(0, self.actualizar_pantalla)
                time.sleep(self.velocidad / 1000)
                
            self.modo_auto = False
            self.root.after(0, self.habilitar_botones)
            
        threading.Thread(target=ejecutar_automaticamente, daemon=True).start()
        
    def reiniciar_maquina(self):
        self.modo_auto = False
        self.mt = None
        self.actualizar_pantalla()
        self.texto_historial.config(state='normal')
        self.texto_historial.delete(1.0, tk.END)
        self.texto_historial.config(state='disabled')
        
    def habilitar_botones(self):
        self.boton_ejecutar.config(state='normal')
        self.boton_paso.config(state='normal')
        
    def actualizar_pantalla(self):
        if not self.mt:
            self.etiqueta_estado.config(text="Listo para comenzar", foreground='#4FA6FF')
            self.etiqueta_pasos.config(text="Pasos: 0")
            self.etiqueta_estado_actual.config(text="Estado: -")
            self.dibujar_cinta([], 0)
            return
            
        estado = self.mt.obtener_estado_actual()
        color_estado = '#4CAF50' if estado == "ACEPTADA" else '#F44336' if estado == "RECHAZADA" else '#4FA6FF'
        
        self.etiqueta_estado.config(text=f"Estado: {estado}", foreground=color_estado)
        self.etiqueta_pasos.config(text=f"Pasos: {self.mt.contador_pasos}")
        self.etiqueta_estado_actual.config(text=f"Estado Actual: {self.mt.estado_actual}")
        
        self.dibujar_cinta(self.mt.cinta, self.mt.posicion_cabezal)
        
    def dibujar_cinta(self, cinta, pos_cabezal):
        self.lienzo_cinta.delete("all")
        
        if not cinta:
            return
            
        ancho_celda = 60
        alto_celda = 60
        inicio_x = 50
        inicio_y = 80
        
        # Dibujar celdas de la cinta
        for i, simbolo in enumerate(cinta):
            x = inicio_x + i * ancho_celda
            y = inicio_y
            
            # Fondo de celda
            color = '#3C3C3C'
            if i == pos_cabezal:
                color = '#0078D4'  # Resaltar posición del cabezal
                
            self.lienzo_cinta.create_rectangle(x, y, x + ancho_celda, y + alto_celda, 
                                             fill=color, outline='#666666', width=2)
            
            # Símbolo
            self.lienzo_cinta.create_text(x + ancho_celda/2, y + alto_celda/2, 
                                        text=simbolo, fill='white', font=('Segoe UI', 14, 'bold'))
            
            # Indicador de posición
            self.lienzo_cinta.create_text(x + ancho_celda/2, y + alto_celda + 10, 
                                        text=str(i), fill='#CCCCCC', font=('Segoe UI', 8))
        
        # Dibujar cabezal
        cabeza_x = inicio_x + pos_cabezal * ancho_celda + ancho_celda/2
        cabeza_y = inicio_y - 20
        self.lienzo_cinta.create_polygon(
            cabeza_x, cabeza_y,
            cabeza_x - 10, cabeza_y - 15,
            cabeza_x + 10, cabeza_y - 15,
            fill='#FF6B6B', outline='white'
        )
        
        # Etiqueta del cabezal
        self.lienzo_cinta.create_text(cabeza_x, cabeza_y - 25, text="Cabezal", 
                                    fill='#FF6B6B', font=('Segoe UI', 9, 'bold'))
        
    def agregar_al_historial(self, mensaje):
        self.texto_historial.config(state='normal')
        self.texto_historial.insert(tk.END, f"{mensaje}\n")
        self.texto_historial.see(tk.END)
        self.texto_historial.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazMaquinaTuring(root)
    root.mainloop()