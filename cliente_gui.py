"""
Cliente Grafico (GUI) de Mensajeria con Cifrado Blowfish
Materia: Redes II - Proyecto Integrador
Permite conexion a servidores locales o remotos (LAN / Wi-Fi / Internet).
"""

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, ttk
from cifrado_blowfish import cifrar_mensaje, descifrar_mensaje

class DialogoConexion(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Conectar a Servidor - Redes II")
        self.geometry("380x250")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self.transient(parent)
        self.grab_set()

        self.resultado = None

        lbl_tit = tk.Label(self, text="Parametros de Conexion TCP", fg="#89b4fa", bg="#1e1e2e", font=("Arial", 11, "bold"))
        lbl_tit.pack(pady=10)

        # Campos
        frame_form = tk.Frame(self, bg="#1e1e2e")
        frame_form.pack(padx=20, pady=5, fill=tk.X)

        tk.Label(frame_form, text="Nombre/Alias:", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=4)
        self.txt_nombre = tk.Entry(frame_form, bg="#313244", fg="#ffffff", insertbackground="white", font=("Arial", 9))
        self.txt_nombre.insert(0, "Estudiante")
        self.txt_nombre.grid(row=0, column=1, sticky="ew", pady=4, padx=5)

        tk.Label(frame_form, text="IP del Servidor:", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=4)
        self.txt_ip = tk.Entry(frame_form, bg="#313244", fg="#ffffff", insertbackground="white", font=("Arial", 9))
        self.txt_ip.insert(0, "127.0.0.1")
        self.txt_ip.grid(row=1, column=1, sticky="ew", pady=4, padx=5)

        tk.Label(frame_form, text="Puerto TCP:", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 9)).grid(row=2, column=0, sticky="w", pady=4)
        self.txt_puerto = tk.Entry(frame_form, bg="#313244", fg="#ffffff", insertbackground="white", font=("Arial", 9))
        self.txt_puerto.insert(0, "5000")
        self.txt_puerto.grid(row=2, column=1, sticky="ew", pady=4, padx=5)

        frame_form.columnconfigure(1, weight=1)

        lbl_ayuda = tk.Label(self, text="* Para conectar desde otra PC en la misma red Wi-Fi,\ningresa la IP del servidor (ej. 192.168.1.x)", fg="#a6adc8", bg="#1e1e2e", font=("Arial", 8))
        lbl_ayuda.pack(pady=5)

        btn_conectar = tk.Button(self, text="Conectar al Chat", bg="#89b4fa", fg="#11111b", font=("Arial", 10, "bold"), command=self.confirmar)
        btn_conectar.pack(pady=10)

        self.bind("<Return>", lambda e: self.confirmar())

    def confirmar(self):
        nombre = self.txt_nombre.get().strip() or "Usuario"
        ip = self.txt_ip.get().strip() or "127.0.0.1"
        try:
            puerto = int(self.txt_puerto.get().strip())
        except ValueError:
            puerto = 5000
        self.resultado = (nombre, ip, puerto)
        self.destroy()

class ChatClienteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mensajeria Segura - Algoritmo Blowfish (Redes II)")
        self.root.geometry("680x620")
        self.root.configure(bg="#1e1e2e")

        self.socket_cliente = None
        self.nombre_usuario = ""
        self.servidor_ip = "127.0.0.1"
        self.servidor_puerto = 5000

        self.pedir_parametros()
        if not self.nombre_usuario:
            self.root.destroy()
            return

        self.crear_interfaz()
        self.conectar_servidor()

    def pedir_parametros(self):
        dialogo = DialogoConexion(self.root)
        self.root.wait_window(dialogo)
        if dialogo.resultado:
            self.nombre_usuario, self.servidor_ip, self.servidor_puerto = dialogo.resultado
            self.root.title(f"Chat Seguro Blowfish - {self.nombre_usuario} @ {self.servidor_ip}:{self.servidor_puerto}")
        else:
            self.nombre_usuario = None

    def crear_interfaz(self):
        # Barra superior con datos de conexion y algoritmo
        frame_top = tk.Frame(self.root, bg="#2b2b3d", pady=8)
        frame_top.pack(fill=tk.X)
        lbl_titulo = tk.Label(frame_top, text="PROYECTO INTEGRADOR - REDES II", fg="#89b4fa", bg="#2b2b3d", font=("Arial", 12, "bold"))
        lbl_titulo.pack()
        lbl_sub = tk.Label(frame_top, text=f"Servidor: {self.servidor_ip}:{self.servidor_puerto} | Cifrado: Blowfish CBC (128 bits)", fg="#cdd6f4", bg="#2b2b3d", font=("Arial", 9))
        lbl_sub.pack()

        # Area de Chat
        lbl_chat = tk.Label(self.root, text="Bandeja de Mensajes (Descifrados en Destino):", fg="#a6adc8", bg="#1e1e2e", font=("Arial", 10, "bold"), anchor="w")
        lbl_chat.pack(fill=tk.X, padx=15, pady=(8, 0))

        self.area_chat = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=13, bg="#11111b", fg="#cdd6f4", font=("Consolas", 10))
        self.area_chat.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        self.area_chat.config(state=tk.DISABLED)

        # Monitor de Red (Datos cifrados en transito)
        lbl_monitor = tk.Label(self.root, text="Monitor de Red / Criptografia (Cuerpo Cifrado Blowfish en Hexadecimal):", fg="#f38ba8", bg="#1e1e2e", font=("Arial", 10, "bold"), anchor="w")
        lbl_monitor.pack(fill=tk.X, padx=15, pady=(5, 0))

        self.area_monitor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=6, bg="#181825", fg="#a6e3a1", font=("Consolas", 9))
        self.area_monitor.pack(padx=15, pady=5, fill=tk.X)
        self.area_monitor.config(state=tk.DISABLED)

        # Entrada de texto y boton enviar
        frame_input = tk.Frame(self.root, bg="#1e1e2e", pady=10)
        frame_input.pack(fill=tk.X, padx=15)

        self.entrada_msg = tk.Entry(frame_input, bg="#313244", fg="#ffffff", insertbackground="white", font=("Arial", 11))
        self.entrada_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        self.entrada_msg.bind("<Return>", lambda event: self.enviar_mensaje())

        btn_enviar = tk.Button(frame_input, text="Cifrar y Enviar", bg="#89b4fa", fg="#11111b", font=("Arial", 10, "bold"), command=self.enviar_mensaje, padx=15, pady=3)
        btn_enviar.pack(side=tk.RIGHT)

    def conectar_servidor(self):
        try:
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.connect((self.servidor_ip, self.servidor_puerto))
            self.agregar_chat(f"[*] Conectado exitosamente al servidor {self.servidor_ip}:{self.servidor_puerto}\n")
            self.agregar_chat(f"[*] Canal seguro Blowfish inicializado con exito.\n")
            
            hilo_recibir = threading.Thread(target=self.recibir_mensajes, daemon=True)
            hilo_recibir.start()
        except Exception as e:
            messagebox.showerror("Error de Conexion", f"No se pudo conectar a {self.servidor_ip}:{self.servidor_puerto}\n\nDetalle: {e}\n\nVerifica que servidor.py este corriendo en esa IP y que el Firewall permita el puerto {self.servidor_puerto}.")
            self.root.destroy()

    def enviar_mensaje(self):
        texto = self.entrada_msg.get().strip()
        if not texto:
            return

        mensaje_formateado = f"{self.nombre_usuario}: {texto}"
        try:
            # Cifrado Blowfish
            paquete_cifrado = cifrar_mensaje(mensaje_formateado)
            
            # Enviar por socket TCP
            self.socket_cliente.sendall(paquete_cifrado)
            
            # Mostrar localmente
            self.agregar_chat(f"[Tu]: {texto}\n")
            self.agregar_monitor(f"[SALIDA] Enviando {len(paquete_cifrado)}B cifrados: {paquete_cifrado.hex()}\n")
            self.entrada_msg.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar mensaje: {e}")

    def recibir_mensajes(self):
        while True:
            try:
                datos = self.socket_cliente.recv(4096)
                if not datos:
                    break
                
                # Mostrar en monitor de red los bytes cifrados en crudo
                self.agregar_monitor(f"[ENTRADA] Recibidos {len(datos)}B cifrados: {datos.hex()}\n")
                
                # Descifrar con Blowfish
                texto_descifrado = descifrar_mensaje(datos)
                self.agregar_chat(f"{texto_descifrado}\n")
            except Exception as e:
                self.agregar_chat(f"[!] Desconexion del servidor: {e}\n")
                break

    def agregar_chat(self, texto):
        self.area_chat.config(state=tk.NORMAL)
        self.area_chat.insert(tk.END, texto)
        self.area_chat.see(tk.END)
        self.area_chat.config(state=tk.DISABLED)

    def agregar_monitor(self, texto):
        self.area_monitor.config(state=tk.NORMAL)
        self.area_monitor.insert(tk.END, texto)
        self.area_monitor.see(tk.END)
        self.area_monitor.config(state=tk.DISABLED)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = ChatClienteGUI(ventana)
    if app.nombre_usuario:
        ventana.mainloop()
