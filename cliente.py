"""
Cliente de Mensajeria TCP por Consola con Cifrado Blowfish
Materia: Redes II - Proyecto Integrador

Permite conectarse a un servidor local o remoto especificando su IP.
Cifra todos los mensajes con Blowfish CBC antes de enviarlos.
"""

import socket
import threading
import sys
from cifrado_blowfish import cifrar_mensaje, descifrar_mensaje

def recibir_mensajes(socket_cliente):
    """Hilo encargado de escuchar paquetes entrantes y descifrarlos."""
    while True:
        try:
            datos_cifrados = socket_cliente.recv(4096)
            if not datos_cifrados:
                print("\n[!] Conexion con el servidor terminada.")
                break
            
            # 1. Mostrar paquete recibido en crudo (cifrado)
            print("\n" + "-"*50)
            print(f"[RECEPTOR] Paquete recibido de la red ({len(datos_cifrados)} bytes):")
            print(f"HEX Cifrado: {datos_cifrados.hex()[:40]}... (Blowfish)")
            
            # 2. Descifrar con Blowfish
            mensaje_descifrado = descifrar_mensaje(datos_cifrados)
            print(f"[MENSAJE RECIBIDO]: {mensaje_descifrado}")
            print("-" * 50)
            print("> ", end="", flush=True)
            
        except Exception as e:
            print(f"\n[!] Error al recibir o descifrar: {e}")
            break

def iniciar_cliente():
    """Inicia la conexion al servidor (local o remoto) y gestiona el chat."""
    print("="*55)
    print("   CLIENTE DE MENSAJERIA SEGURA - ALGORITMO BLOWFISH")
    print("="*55)
    
    # 1. Nombre de usuario
    nombre_usuario = input("Tu nombre o alias: ").strip()
    if not nombre_usuario:
        nombre_usuario = "Usuario"

    # 2. IP del Servidor
    ip_servidor = input("IP del Servidor (Presiona Enter para 127.0.0.1): ").strip()
    if not ip_servidor:
        ip_servidor = "127.0.0.1"

    # 3. Puerto
    puerto_str = input("Puerto del Servidor (Presiona Enter para 5000): ").strip()
    puerto = int(puerto_str) if puerto_str.isdigit() else 5000

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"\n[*] Conectando a {ip_servidor}:{puerto}...")
        cliente.connect((ip_servidor, puerto))
        print(f"[+] ¡Conectado exitosamente con {ip_servidor}!")
    except Exception as e:
        print(f"[-] No se pudo conectar a {ip_servidor}:{puerto}.")
        print(f"    Detalle del error: {e}")
        print("    Verifica que el servidor este encendido y que el Firewall permita el puerto 5000.")
        return

    # Iniciar hilo de recepcion
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True)
    hilo_recibir.start()

    print("\n" + "="*50)
    print("  CANAL CIFRADO ACTIVO (Blowfish CBC - 128 bits)")
    print("  Escribe tu mensaje y presiona Enter para enviar.")
    print("  Escribe 'salir' para cerrar la sesion.")
    print("="*50 + "\n")

    try:
        while True:
            mensaje = input("> ")
            if mensaje.strip().lower() == "salir":
                break
            if not mensaje.strip():
                continue

            formato_mensaje = f"{nombre_usuario}: {mensaje}"
            
            # Cifrar con Blowfish
            paquete_cifrado = cifrar_mensaje(formato_mensaje)
            
            # Mostrar traza didactica en consola
            print(f"  -> Cifrando con Blowfish (IV + CBC)...")
            print(f"  -> Bytes cifrados a enviar: {paquete_cifrado.hex()[:40]}...")
            
            # Enviar por el socket TCP
            cliente.sendall(paquete_cifrado)

    except KeyboardInterrupt:
        print("\n[!] Saliendo...")
    finally:
        cliente.close()
        print("[-] Conexion cerrada.")

if __name__ == "__main__":
    iniciar_cliente()
