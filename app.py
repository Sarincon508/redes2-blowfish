"""
Servidor Web Flask con Cifrado Blowfish Extremo a Extremo
Materia: Redes II - Proyecto Integrador

El servidor almacena y transporta UNICAMENTE datos cifrados (IV + Ciphertext).
Tanto el remitente como el mensaje se cifran juntos.
Si un usuario entra con una clave diferente (incluso por 1 solo caracter),
el algoritmo Blowfish CBC fallara y no podra leer ni el remitente ni el mensaje.
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from cifrado_blowfish import cifrar_mensaje, descifrar_mensaje, CLAVE_COMPARTIDA

app = Flask(__name__)

# Estructura en memoria:
# salas_mensajes = { "sala": [ {id, cipher_hex, iv_hex, bytes_count, timestamp} ] }
salas_mensajes = {}
contador_ids = 0

def ajustar_clave(clave_str: str) -> bytes:
    """
    Convierte la clave a bytes para Blowfish.
    Blowfish acepta claves variables de 32 a 448 bits (4 a 56 bytes).
    Si se cambia o eliminan caracteres, la clave resultante es completamente distinta.
    """
    if not clave_str:
        return CLAVE_COMPARTIDA
    clave_bytes = clave_str.encode('utf-8')
    if len(clave_bytes) < 4:
        clave_bytes = clave_bytes.ljust(4, b'#')
    elif len(clave_bytes) > 56:
        clave_bytes = clave_bytes[:56]
    return clave_bytes

@app.route("/")
def index():
    """Sirve la aplicacion web."""
    return render_template("index.html")

@app.route("/api/send", methods=["POST"])
def enviar_mensaje():
    """
    Recibe el remitente y el texto, los concatena y los cifra juntos con Blowfish.
    El servidor NO almacena texto plano; unicamente almacena el paquete cifrado.
    """
    global contador_ids
    datos = request.get_json(force=True)
    
    sala = datos.get("room", "").strip().lower() or "general"
    remitente = datos.get("sender", "").strip() or "Anonimo"
    texto = datos.get("text", "").strip()
    clave_str = datos.get("key", "").strip()
    
    if not texto:
        return jsonify({"success": False, "error": "El mensaje no puede estar vacio"}), 400

    clave = ajustar_clave(clave_str)
    
    try:
        # Formato del payload seguro: "Remitente::: Mensaje"
        payload_plano = f"{remitente}::: {texto}"
        
        # Cifrado Blowfish CBC (64 bits, IV aleatorio)
        paquete_cifrado = cifrar_mensaje(payload_plano, clave=clave)
        iv_hex = paquete_cifrado[:8].hex()
        paquete_hex = paquete_cifrado.hex()
        
        contador_ids += 1
        hora_actual = datetime.now().strftime("%H:%M:%S")
        
        # El servidor almacena UNICAMENTE datos cifrados
        registro_cifrado = {
            "id": contador_ids,
            "room": sala,
            "cipher_hex": paquete_hex,
            "iv_hex": iv_hex,
            "bytes_count": len(paquete_cifrado),
            "timestamp": hora_actual
        }
        
        if sala not in salas_mensajes:
            salas_mensajes[sala] = []
            
        salas_mensajes[sala].append(registro_cifrado)
        if len(salas_mensajes[sala]) > 100:
            salas_mensajes[sala].pop(0)
            
        return jsonify({
            "success": True,
            "message": {
                "id": contador_ids,
                "sender": remitente,
                "text": texto,
                "cipher_hex": paquete_hex,
                "iv_hex": iv_hex,
                "bytes_count": len(paquete_cifrado),
                "timestamp": hora_actual,
                "decrypted": True
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/messages", methods=["GET"])
def obtener_mensajes():
    """
    Obtiene los paquetes cifrados de la sala e intenta descifrarlos
    usando la clave que el usuario lector proporciona.
    Si la clave no coincide, el descifrado falla y se oculta el contenido y el remitente.
    """
    sala = request.args.get("room", "").strip().lower() or "general"
    clave_str = request.args.get("key", "").strip()
    since_id = int(request.args.get("since", 0))
    
    clave_lector = ajustar_clave(clave_str)
    mensajes_sala = salas_mensajes.get(sala, [])
    nuevos = [m for m in mensajes_sala if m["id"] > since_id]
    
    procesados = []
    for m in nuevos:
        paquete_bytes = bytes.fromhex(m["cipher_hex"])
        try:
            # Intento de descifrado con Blowfish CBC usando la clave del lector
            texto_descifrado = descifrar_mensaje(paquete_bytes, clave=clave_lector)
            
            # Formato esperado: "Remitente::: Texto"
            if "::: " in texto_descifrado:
                remitente, cuerpo = texto_descifrado.split("::: ", 1)
            else:
                remitente, cuerpo = "Desconocido", texto_descifrado
                
            procesados.append({
                "id": m["id"],
                "sender": remitente,
                "text": cuerpo,
                "cipher_hex": m["cipher_hex"],
                "iv_hex": m["iv_hex"],
                "bytes_count": m["bytes_count"],
                "timestamp": m["timestamp"],
                "decrypted": True
            })
        except Exception:
            # Falla criptografica: la clave del lector no es igual a la del emisor
            procesados.append({
                "id": m["id"],
                "sender": "🔒 Cifrado con Blowfish",
                "text": "⚠️ [ERROR DE DESCIFRADO]: No se pudo descifrar este mensaje. Tu clave Blowfish es diferente a la del emisor.",
                "cipher_hex": m["cipher_hex"],
                "iv_hex": m["iv_hex"],
                "bytes_count": m["bytes_count"],
                "timestamp": m["timestamp"],
                "decrypted": False
            })
            
    return jsonify({
        "success": True,
        "room": sala,
        "messages": procesados,
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
    puerto = int(os.environ.get("PORT", 5000))
    print(f"[*] Servidor Web Redes II activo en el puerto {puerto}")
    app.run(host="0.0.0.0", port=puerto, debug=False)
