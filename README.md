# Aplicación de Mensajería Segura con Cifrado Blowfish
**Materia:** Redes II  
**Proyecto:** Proyecto Integrador - Seguridad en la Capa de Transporte y Aplicación  
**Ubicación:** `F:\Users\Max\Desktop\redes`

---

## 📌 1. Descripción del Proyecto
Esta es una aplicación cliente-servidor desarrollada en Python utilizando sockets TCP y el algoritmo criptográfico simétrico **Blowfish**. Su propósito principal es demostrar cómo garantizar la **confidencialidad de los datos en tránsito** a través de una red local o en la nube, evitando que atacantes con herramientas de captura de paquetes (como Wireshark) puedan leer los mensajes en texto plano.

---

## 📁 2. Estructura de Archivos

```
F:\Users\Max\Desktop\redes\
│
├── cifrado_blowfish.py              # Módulo criptográfico (Blowfish CBC - 128 bits)
│
├── servidor.py                      # Servidor TCP local / LAN (escucha en 0.0.0.0:5000)
├── cliente.py                       # Cliente TCP por consola
├── cliente_gui.py                   # Cliente TCP gráfico Tkinter (con selector de IP)
│
├── servidor_cloud.py                # Servidor para desplegar GRATIS en la NUBE (Render, Railway, etc.)
├── cliente_cloud_gui.py             # Cliente gráfico para conectarse al servidor en la NUBE
├── requirements.txt                 # Dependencias para despliegue en la nube
│
├── DESPLIEGUE_SERVIDOR_GRATUITO.md  # Paso a paso para subirlo a Render.com o usar Ngrok gratis
├── GUIA_CONEXION_DOS_DISPOSITIVOS.md# Instrucciones para conectar 2 PCs en la misma red Wi-Fi
├── guion_video_10min.md             # Guión estructurado para el video de YouTube de 10 min
└── README.md                        # Esta documentación
```

---

## 🚀 3. ¿Cómo usarlo según tu necesidad?

### A. Para dos dispositivos en la misma casa / red Wi-Fi (Sin internet externa):
1. En la PC 1 corre: `python servidor.py` (anota la IP que te muestra, ej: `192.168.1.2`).
2. En la PC 2 corre: `python cliente_gui.py` e ingresa la IP de la PC 1.

### B. Para dos dispositivos en casas diferentes (Despliegue 100% Gratis en la Nube):
1. Sube `servidor_cloud.py`, `cifrado_blowfish.py` y `requirements.txt` a **Render.com** (ver [DESPLIEGUE_SERVIDOR_GRATUITO.md](file:///F:/Users/Max/Desktop/redes/DESPLIEGUE_SERVIDOR_GRATUITO.md)).
2. Abre `cliente_cloud_gui.py` en ambas computadoras e ingresa la URL de Render (ej. `wss://tu-chat.onrender.com`).
