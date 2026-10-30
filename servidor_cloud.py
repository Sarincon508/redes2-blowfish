"""
Servidor en la Nube (WebSocket sobre TCP) con Cifrado Blowfish
Compatible con despliegue gratuito en: Render.com, Railway, Fly.io, etc.
Materia: Redes II - Proyecto Integrador
"""

import os
import asyncio
import websockets
from cifrado_blowfish import descifrar_mensaje

# Render y la mayoria de nubes asignan el puerto a traves de la variable de entorno PORT
PUERTO = int(os.environ.get("PORT", 8765))
HOST = "0.0.0.0"

# Conjunto de clientes conectados a la nube
clientes = set()

async def manejar_cliente(websocket):
    clientes.add(websocket)
    ip_origen = websocket.remote_address[0] if websocket.remote_address else "Remoto"
    print(f"\n[+] Nuevo dispositivo conectado desde {ip_origen}. Total activos: {len(clientes)}")
    
    try:
        async for mensaje_cifrado in websocket:
            # mensaje_cifrado llega como bytes o hex
            if isinstance(mensaje_cifrado, str):
                datos_cifrados = bytes.fromhex(mensaje_cifrado)
            else:
                datos_cifrados = mensaje_cifrado

            print("\n" + "="*65)
            print(f"[PAQUETE EN LA NUBE] Recibidos {len(datos_cifrados)} bytes")
            print(f"Cuerpo cifrado (HEX): {datos_cifrados.hex()}")
            
            try:
                texto = descifrar_mensaje(datos_cifrados)
                print(f"[INSPECCION EN SERVIDOR CLOUD]: {texto}")
            except Exception as e:
                print(f"[INSPECCION]: Error al descifrar: {e}")
            print("="*65)
            
            # Retransmitir el paquete cifrado a todos los demas clientes en la nube
            destinatarios = [c for c in clientes if c != websocket]
            if destinatarios:
                # Enviamos el hex para maxima compatibilidad websocket
                await asyncio.gather(*[c.send(datos_cifrados.hex()) for c in destinatarios])
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clientes.remove(websocket)
        print(f"[-] Dispositivo desconectado. Total activos: {len(clientes)}")

async def main():
    print("*"*65)
    print("   SERVIDOR CLOUD DE MENSAJERIA SEGURA - BLOWFISH")
    print("        Proyecto Integrador - Redes II")
    print("*"*65)
    print(f"[*] Iniciando servidor en {HOST}:{PUERTO}...")
    
    async with websockets.serve(manejar_cliente, HOST, PUERTO):
        print(f"[*] Servidor activo y listo para recibir conexiones en la nube.")
        await asyncio.Future()  # Mantener corriendo para siempre

if __name__ == "__main__":
    asyncio.run(main())
