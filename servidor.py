"""
Servidor de Mensajeria TCP con Cifrado Blowfish
Materia: Redes II - Proyecto Integrador

Este servidor escucha en un socket TCP en TODAS las interfaces de red (0.0.0.0),
permitiendo conexiones locales (127.0.0.1), desde otros dispositivos en la misma
red Wi-Fi/LAN (ej. 192.168.x.x) o desde internet si se usa un VPS o tunel.
"""

import socket
import threading
from cifrado_blowfish import descifrar_mensaje

# 0.0.0.0 permite que el servidor acepte conexiones desde cualquier interfaz de red
HOST = "0.0.0.0"
PUERTO = 5000

# Lista de clientes conectados
clientes_conectados = []
lock = threading.Lock()

def obtener_ips_locales():
    """Detecta las direcciones IP locales para mostrarle al usuario como conectarse."""
    ips = []
    try:
        # Intentar obtener la IP conectandose temporalmente a un socket UDP falso
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.append(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    
    # Agregar hostname IP por si acaso
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
        if host_ip not in ips and not host_ip.startswith("127."):
            ips.append(host_ip)
    except Exception:
        pass
    return ips

def retransmitir(mensaje_cifrado, remitente_socket):
    """Envia el paquete cifrado a todos los clientes excepto al que lo envio."""
    with lock:
        for cliente in clientes_conectados:
            if cliente != remitente_socket:
                try:
                    cliente.sendall(mensaje_cifrado)
                except Exception:
                    clientes_conectados.remove(cliente)

def manejar_cliente(socket_cliente, direccion):
    """Atiende la comunicacion de un cliente conectado."""
    print(f"\n[+] NUEVA CONEXION ENTRANTE desde {direccion[0]}:{direccion[1]}")
    with lock:
        clientes_conectados.append(socket_cliente)
        print(f"[*] Dispositivos conectados en la sala: {len(clientes_conectados)}")
        
    try:
        while True:
            # Recibir datos del socket (paquete cifrado Blowfish)
            datos_recibidos = socket_cliente.recv(4096)
            if not datos_recibidos:
                break
            
            # Demostracion para Redes II:
            print("\n" + "="*65)
            print(f"[PAQUETE DE RED RECIBIDO] Dispositivo: {direccion[0]}:{direccion[1]}")
            print(f"Tamano del payload TCP: {len(datos_recibidos)} bytes")
            print(f"Cuerpo cifrado (HEX): {datos_recibidos.hex()}")
            
            # Inspeccion pedagogica:
            try:
                texto_descifrado = descifrar_mensaje(datos_recibidos)
                print(f"[CONTENIDO DESCIFRADO CON CLAVE]: {texto_descifrado}")
            except Exception as e:
                print(f"[INSPECCION]: Error de clave o integridad: {e}")
            print("="*65)
            
            # Retransmitir el paquete cifrado intacto a los demas dispositivos
            retransmitir(datos_recibidos, socket_cliente)
            
    except ConnectionResetError:
        print(f"[-] Conexion cerrada abruptamente por {direccion[0]}:{direccion[1]}")
    finally:
        with lock:
            if socket_cliente in clientes_conectados:
                clientes_conectados.remove(socket_cliente)
        socket_cliente.close()
        print(f"[-] Dispositivo desconectado ({direccion[0]}). Conectados actuales: {len(clientes_conectados)}")

def iniciar_servidor():
    """Inicia el servidor TCP y muestra las IPs de conexion."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind((HOST, PUERTO))
        servidor.listen(10)
        
        ips = obtener_ips_locales()
        print("*"*65)
        print("      SERVIDOR DE MENSAJERIA SEGURA - BLOWFISH")
        print("          Proyecto Integrador - Redes II")
        print("*"*65)
        print(f"[*] Escuchando en el puerto TCP: {PUERTO}")
        print("[*] Direcciones IP disponibles para conectar otros dispositivos:")
        print(f"    - Desde esta misma PC (Local):     127.0.0.1")
        for ip in ips:
            print(f"    - Desde otro dispositivo (Wi-Fi/LAN): {ip}")
        print("*"*65)
        print("[*] Esperando conexiones de dispositivos...\n")
        
        while True:
            socket_cliente, direccion = servidor.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(socket_cliente, direccion), daemon=True)
            hilo.start()
            
    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario.")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()
