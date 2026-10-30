"""
Servidor Web Flask con Cifrado Blowfish
Materia: Redes II - Proyecto Integrador
Despliegue Web 100% en la Nube (Render.com, Railway, etc.)
Permite salas privadas para mensajearse con personas especificas desde cualquier navegador o movil.
"""

import os
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from cifrado_blowfish import cifrar_mensaje, descifrar_mensaje, CLAVE_COMPARTIDA

app = Flask(__name__)

# Estructura en memoria para salas privadas:
# salas = { "nombre_sala": [ {id, remitente, texto, cipher_hex, iv_hex, hora} ] }
salas_mensajes = {}
contador_ids = 0

def ajustar_clave(clave_str: str) -> bytes:
    """Ajusta una clave dada por el usuario a un tamano valido para Blowfish (16 bytes = 128 bits)."""
    if not clave_str:
        return CLAVE_COMPARTIDA
    clave_bytes = clave_str.encode('utf-8')
    if len(clave_bytes) < 4:
        clave_bytes = clave_bytes.ljust(16, b'#')
    elif len(clave_bytes) > 56:  # Limite maximo de Blowfish es 448 bits = 56 bytes
        clave_bytes = clave_bytes[:56]
    return clave_bytes

@app.route("/")
def index():
    """Sirve la aplicacion web de mensajeria."""
    return render_template("index.html")

@app.route("/api/send", methods=["POST"])
def enviar_mensaje():
    """Recibe un mensaje de la web, lo cifra con Blowfish y lo almacena en la sala correspondiente."""
    global contador_ids
    datos = request.get_json(force=True)
    
    sala = datos.get("room", "").strip().lower() or "general"
    remitente = datos.get("sender", "").strip() or "Anonimo"
    texto = datos.get("text", "").strip()
    clave_personalizada = datos.get("key", "").strip()
    
    if not texto:
        return jsonify({"success": False, "error": "El mensaje no puede estar vacio"}), 400

    clave = ajustar_clave(clave_personalizada)
    
    try:
        # Cifrado Blowfish CBC (64 bits, IV aleatorio)
        paquete_cifrado = cifrar_mensaje(texto, clave=clave)
        iv_hex = paquete_cifrado[:8].hex()
        cuerpo_cifrado_hex = paquete_cifrado[8:].hex()
        paquete_completo_hex = paquete_cifrado.hex()
        
        contador_ids += 1
        hora_actual = datetime.now().strftime("%H:%M:%S")
        
        mensaje_obj = {
            "id": contador_ids,
            "room": sala,
            "sender": remitente,
            "text": texto,  # Texto descifrado para mostrar al usuario autorizado
            "cipher_hex": paquete_completo_hex,
            "iv_hex": iv_hex,
            "body_hex": cuerpo_cifrado_hex,
            "bytes_count": len(paquete_cifrado),
            "timestamp": hora_actual
        }
        
        if sala not in salas_mensajes:
            salas_mensajes[sala] = []
            
        salas_mensajes[sala].append(mensaje_obj)
        # Mantener maximo ultimos 100 mensajes por sala
        if len(salas_mensajes[sala]) > 100:
            salas_mensajes[sala].pop(0)
            
        return jsonify({"success": True, "message": mensaje_obj})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/messages", methods=["GET"])
def obtener_mensajes():
    """Obtiene los mensajes de una sala especifica con ID mayor a 'since'."""
    sala = request.args.get("room", "").strip().lower() or "general"
    since_id = int(request.args.get("since", 0))
    
    mensajes_sala = salas_mensajes.get(sala, [])
    nuevos = [m for m in mensajes_sala if m["id"] > since_id]
    
    return jsonify({
        "success": True,
        "room": sala,
        "messages": nuevos,
        "total": len(mensajes_sala)
    })

@app.route("/api/clear", methods=["POST"])
def limpiar_sala():
    """Limpia el historial de una sala especifica."""
    datos = request.get_json(force=True)
    sala = datos.get("room", "").strip().lower() or "general"
    salas_mensajes[sala] = []
    return jsonify({"success": True, "message": f"Sala {sala} vaciada"})

if __name__ == "__main__":
    # Puerto dinamico para despliegues en la nube (Render, Railway, etc.)
    puerto = int(os.environ.get("PORT", 5000))
    print(f"[*] Servidor Web Redes II activo en el puerto {puerto}")
    app.run(host="0.0.0.0", port=puerto, debug=False)
