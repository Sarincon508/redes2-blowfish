"""
Cliente Grafico para Servidor en la Nube (Render / WebSockets)
Cifrado Simetrico Blowfish (Modo CBC - 128 bits)
Materia: Redes II - Proyecto Integrador
"""

import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import websockets
from cifrado_blowfish import cifrar_mensaje, descifrar_mensaje

class DialogoCloud(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Conexion al Servidor Cloud")
        self.geometry("450x230")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self.transient(parent)
        self.grab_set()

        self.resultado = None

        lbl_tit = tk.Label(self, text="Parametros de Conexion a la Nube", fg="#89b4fa", bg="#1e1e2e", font=("Arial", 11, "bold"))
        lbl_tit.pack(pady=10)

        frame = tk.Frame(self, bg="#1e1e2e")
        frame.pack(padx=20, pady=5, fill=tk.X)

        tk.Label(frame, text="Nombre/Alias:", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nombre = tk.Entry(frame, bg="#313244", fg="#ffffff", insertbackground="white", font=("Arial", 9))
        self.txt_nombre.insert(0, "Estudiante")
        self.txt_nombre.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame, text="URL del Servidor:", fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.txt_url = tk.Entry(frame, bg="#313244", fg="#ffffff", insertbackground="white", font=("Arial", 9))
        # URL por defecto o ejemplo de Render
        self.txt_url.insert(0, "ws://localhost:8765")
        self.txt_url.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        frame.columnconfigure(1, weight=1)

        lbl_hint = tk.Label(self, text="* Ejemplo en la nube: wss://chat-blowfish.onrender.com\n* Ejemplo local: ws://localhost:8765", fg="#a6adc8", bg="#1e1e2e", font=("Arial", 8))
        lbl_hint.pack(pady=5)

        btn = tk.Button(self, text="Conectar a la Nube", bg="#89b4fa", fg="#11111b", font=("Arial", 10, "bold"), command=self.confirmar)
        btn.pack(pady=10)

        self.bind("<Return>", lambda e: self.confirmar())

    def confirmar(self):
        nombre = self.txt_nombre.get().strip() or "Usuario"
        url = self.txt_url.get().strip() or "ws://localhost:8765"
        self.resultado = (nombre, url)
        self.destroy()

class ChatCloudGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mensajeria Segura Cloud - Blowfish (Redes II)")
        self.root.geometry("680x620")
        self.root.configure(bg="#1e1e2e")

        self.ws = None
        self.loop = None
        self.nombre_usuario = ""
        self.url_servidor = ""

        self.pedir_parametros()
        if not self.nombre_usuario:
            self.root.destroy()
            return

        self.crear_interfaz()
        # Iniciar loop asyncio en un hilo secundario
        self.hilo_async = threading.Thread(target=self.iniciar_hilo_asyncio, daemon=True)
        self.hilo_async.start()

    def pedir_parametros(self):
        d = DialogoCloud(self.root)
        self.root.wait_window(d)
        if d.resultado:
            self.nombre_usuario, self.url_servidor = d.resultado
            self.root.title(f"Chat Cloud Blowfish - {self.nombre_usuario} @ {self.url_servidor}")
        else:
            self.nombre_usuario = None

    def crear_interfaz(self):
        frame_top = tk.Frame(self.root, bg="#2b2b3d", pady=8)
        frame_top.pack(fill=tk.X)
        lbl_titulo = tk.Label(frame_top, text="PROYECTO INTEGRADOR - REDES II (NUBE)", fg="#89b4fa", bg="#2b2b3d", font=("Arial", 12, "bold"))
        lbl_titulo.pack()
        lbl_sub = tk.Label(frame_top, text=f"Servidor Cloud: {self.url_servidor} | Cifrado: Blowfish CBC (128 bits)", fg="#cdd6f4", bg="#2b2b3d", font=("Arial", 9))
        lbl_sub.pack()

        lbl_chat = tk.Label(self.root, text="Bandeja de Mensajes (Descifrados en Destino):", fg="#a6adc8", bg="#1e1e2e", font=("Arial", 10, "bold"), anchor="w")
        lbl_chat.pack(fill=tk.X, padx=15, pady=(8, 0))

        self.area_chat = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=13, bg="#11111b", fg="#cdd6f4", font=("Consolas", 10))
        self.area_chat.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        self.area_chat.config(state=tk.DISABLED)

        lbl_monitor = tk.Label(self.root, text="Monitor de Red / Criptografia (Cuerpo Cifrado Blowfish en Hexadecimal):", fg="#f38ba8", bg="#1e1e2e", font=("Arial", 10, "bold"), anchor="w")
        lbl_monitor.pack(fill=tk.X, padx=15, pady=(5, 0))

        self.area_monitor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=6, bg="#181825", fg="#a6e3a1", font=("Consolas", 9))
        self.area_monitor.pack(padx=15, pady=5, fill=tk.X)
        self.area_monitor.config(state=tk.DISABLED)

        frame_input = tk.Frame(self.root, bg="#1e1e2e", pady=10)
        frame_input.pack(fill=tk.X, padx=15)

        self.entrada_msg = tk.Entry(frame_input, bg="#313244", fg="#ffffff", insertbackground="white", font=("Arial", 11))
        self.entrada_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        self.entrada_msg.bind("<Return>", lambda event: self.enviar_mensaje())

        btn_enviar = tk.Button(frame_input, text="Cifrar y Enviar", bg="#89b4fa", fg="#11111b", font=("Arial", 10, "bold"), command=self.enviar_mensaje, padx=15, pady=3)
        btn_enviar.pack(side=tk.RIGHT)

    def iniciar_hilo_asyncio(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.conectar_cloud())

    async def conectar_cloud(self):
        self.agregar_chat(f"[*] Conectando al servidor cloud: {self.url_servidor}...\n")
        try:
            async with websockets.connect(self.url_servidor) as websocket:
                self.ws = websocket
                self.agregar_chat("[+] ¡Conectado exitosamente a la nube!\n")
                self.agregar_chat("[*] Canal seguro Blowfish CBC activado.\n")
                
                async for mensaje_hex in websocket:
                    try:
                        datos_cifrados = bytes.fromhex(mensaje_hex)
                        self.agregar_monitor(f"[ENTRADA CLOUD] Recibidos {len(datos_cifrados)}B cifrados: {datos_cifrados.hex()}\n")
                        texto = descifrar_mensaje(datos_cifrados)
                        self.agregar_chat(f"{texto}\n")
                    except Exception as e:
                        self.agregar_chat(f"[!] Error al procesar paquete: {e}\n")
        except Exception as e:
            self.agregar_chat(f"[-] No se pudo conectar a la nube: {e}\n")

    def enviar_mensaje(self):
        texto = self.entrada_msg.get().strip()
        if not texto or not self.ws or not self.loop:
            return

        formato = f"{self.nombre_usuario}: {texto}"
        try:
            paquete_cifrado = cifrar_mensaje(formato)
            hex_data = paquete_cifrado.hex()

            # Enviar a traves del loop de asyncio
            asyncio.run_coroutine_threadsafe(self.ws.send(hex_data), self.loop)

            self.agregar_chat(f"[Tu]: {texto}\n")
            self.agregar_monitor(f"[SALIDA CLOUD] Enviando {len(paquete_cifrado)}B cifrados: {hex_data}\n")
            self.entrada_msg.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar: {e}")

    def agregar_chat(self, texto):
        self.root.after(0, self._append_chat, texto)

    def _append_chat(self, texto):
        self.area_chat.config(state=tk.NORMAL)
        self.area_chat.insert(tk.END, texto)
        self.area_chat.see(tk.END)
        self.area_chat.config(state=tk.DISABLED)

    def agregar_monitor(self, texto):
        self.root.after(0, self._append_monitor, texto)

    def _append_monitor(self, texto):
        self.area_monitor.config(state=tk.NORMAL)
        self.area_monitor.insert(tk.END, texto)
        self.area_monitor.see(tk.END)
        self.area_monitor.config(state=tk.DISABLED)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = ChatCloudGUI(ventana)
    if app.nombre_usuario:
        ventana.mainloop()
