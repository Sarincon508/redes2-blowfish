"""
Modulo de Cifrado y Descifrado con Blowfish
Materia: Redes II - Proyecto Integrador

Caracteristicas de Blowfish:
- Cifrador de bloques simetrico (usa la misma clave para cifrar y descifrar).
- Tamano de bloque: 64 bits (8 bytes).
- Longitud de clave: variable de 32 a 448 bits (aqui usamos 128 bits / 16 bytes).
- Modo de operacion: CBC (Cipher Block Chaining) con vector de inicializacion (IV).
"""

import os
# Compatibilidad con diferentes versiones de la libreria cryptography
try:
    from cryptography.hazmat.decrepit.ciphers.algorithms import Blowfish
except ImportError:
    from cryptography.hazmat.primitives.ciphers.algorithms import Blowfish

from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives import padding

# Clave simetrica compartida (16 caracteres = 128 bits)
# Ambos dispositivos deben compartir esta clave.
CLAVE_COMPARTIDA = b"Redes2Clave128B!"

def cifrar_mensaje(texto_plano: str, clave: bytes = CLAVE_COMPARTIDA) -> bytes:
    """
    Cifra un string de texto plano usando Blowfish en modo CBC.
    1. Genera un IV (Vector de Inicializacion) aleatorio de 8 bytes (64 bits).
    2. Aplica relleno PKCS#7 al texto para que sea multiplo de 8 bytes.
    3. Cifra los datos con Blowfish CBC.
    4. Concatena y retorna (IV + datos_cifrados).
    """
    # 1. Blowfish tiene bloques de 64 bits (8 bytes), por lo que el IV es de 8 bytes
    iv = os.urandom(8)
    
    # 2. Relleno PKCS7 para que el mensaje se ajuste a bloques de 64 bits
    padder = padding.PKCS7(64).padder()
    datos_bytes = texto_plano.encode('utf-8')
    datos_con_padding = padder.update(datos_bytes) + padder.finalize()
    
    # 3. Inicializar el cifrador Blowfish en modo CBC
    cifrador = Cipher(Blowfish(clave), modes.CBC(iv))
    encryptor = cifrador.encryptor()
    datos_cifrados = encryptor.update(datos_con_padding) + encryptor.finalize()
    
    # Retornamos el IV pegado al inicio de los datos cifrados
    return iv + datos_cifrados

def descifrar_mensaje(paquete_cifrado: bytes, clave: bytes = CLAVE_COMPARTIDA) -> str:
    """
    Descifra un paquete (IV + datos_cifrados) usando Blowfish en modo CBC.
    1. Extrae los primeros 8 bytes correspondientes al IV.
    2. Descifra el resto de los bytes usando la clave simetrica.
    3. Remueve el relleno PKCS#7.
    4. Retorna el texto plano en UTF-8.
    """
    # 1. Extraer IV (primeros 8 bytes) y ciphertext (resto)
    iv = paquete_cifrado[:8]
    datos_cifrados = paquete_cifrado[8:]
    
    # 2. Inicializar el descifrador
    cifrador = Cipher(Blowfish(clave), modes.CBC(iv))
    decryptor = cifrador.decryptor()
    datos_con_padding = decryptor.update(datos_cifrados) + decryptor.finalize()
    
    # 3. Quitar relleno PKCS7
    unpadder = padding.PKCS7(64).unpadder()
    texto_bytes = unpadder.update(datos_con_padding) + unpadder.finalize()
    
    return texto_bytes.decode('utf-8')

if __name__ == "__main__":
    # Prueba rapida local
    mensaje_original = "Hola mundo desde Redes II"
    print(f"Original: {mensaje_original}")
    
    cifrado = cifrar_mensaje(mensaje_original)
    print(f"Cifrado (hexadecimal que viaja por la red): {cifrado.hex()}")
    
    recuperado = descifrar_mensaje(cifrado)
    print(f"Descifrado en destino: {recuperado}")
