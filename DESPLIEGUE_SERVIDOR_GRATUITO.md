# Guía de Despliegue en Servidores Gratuitos en la Nube
**Materia:** Redes II - Proyecto Integrador  

Aquí tienes las mejores opciones 100% gratuitas para poner tu servidor en internet y que cualquiera pueda conectarse desde su casa o desde cualquier dispositivo.

---

## 🚀 OPCIÓN 1: Render.com (El Servidor queda en la Nube 24/7 sin tu PC)
*(100% Gratuito - No te pide tarjeta de crédito para el plan Free)*

Render permite alojar aplicaciones Python gratis. Como en la nube gratuita el tráfico se maneja por puertos web estándar (HTTP/TLS), hemos creado **`servidor_cloud.py`** y **`cliente_cloud_gui.py`**, los cuales transmiten los paquetes cifrados con **Blowfish** sobre un socket seguro en la nube.

### Pasos para desplegar en Render:

1. **Crear una cuenta gratis:**
   - Entra a [render.com](https://render.com) y regístrate con tu cuenta de GitHub o Google.

2. **Subir los archivos a un repositorio de GitHub:**
   Crea un repositorio (público o privado) en GitHub con estos 4 archivos de tu carpeta `F:\Users\Max\Desktop\redes`:
   - `servidor_cloud.py`
   - `cifrado_blowfish.py`
   - `requirements.txt`
   - `README.md`

3. **Crear el Web Service en Render:**
   - En tu panel de Render, haz clic en **New +** -> **Web Service**.
   - Conecta tu repositorio de GitHub.
   - Configura estos datos:
     - **Name:** `chat-blowfish` (o el que quieras)
     - **Runtime:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python servidor_cloud.py`
     - **Instance Type:** `Free` ($0/mes)
   - Haz clic en **Deploy Web Service**.

4. **Obtener tu URL pública:**
   - Render tardará unos 2 minutos en compilar e iniciar el servidor.
   - Te dará una URL como: `https://chat-blowfish-xxxx.onrender.com`.

5. **Conectarse desde los dos dispositivos:**
   - En cualquier computadora o laptop, abre:
     ```bash
     python cliente_cloud_gui.py
     ```
   - Cambia la URL a formato WebSocket seguro (`wss://`):
     `wss://chat-blowfish-xxxx.onrender.com`
   - ¡Listo! Ambos dispositivos estarán chateando en la nube de Render con cifrado Blowfish extremo a extremo.

---

## ⚡ OPCIÓN 2: Ngrok (Túnel TCP Instantáneo sin subir nada a la nube)
*(Recomendado si quieres usar el `servidor.py` TCP puro sin registrar repositorios)*

Con esta opción, tu `servidor.py` corre en tu máquina, pero se expone a internet a través de un túnel TCP gratuito.

1. Descarga Ngrok gratis desde [ngrok.com](https://ngrok.com) o ejecútalo si ya lo tienes.
2. Inicia tu servidor TCP normalmente en tu PC:
   ```bash
   python servidor.py
   ```
3. En otra terminal ejecuta:
   ```bash
   ngrok tcp 5000
   ```
4. Ngrok te mostrará una dirección pública en pantalla, por ejemplo:
   `Forwarding: tcp://4.tcp.ngrok.io:12345 -> localhost:5000`
5. En el segundo dispositivo (amigo o laptop):
   - Abre `python cliente_gui.py`.
   - En **IP del Servidor** pon: `4.tcp.ngrok.io`
   - En **Puerto** pon: `12345`
   - ¡Conectará al instante a través de internet!

---

## ☁️ OPCIÓN 3: Oracle Cloud Always Free (VPS Linux Gratis de por vida)
*(Ideal si deseas tener una máquina virtual completa en la nube)*

Oracle Cloud ofrece instancias Compute (Ubuntu Linux) con IP pública IPv4 fija gratis para siempre:
1. Creas una instancia en [cloud.oracle.com](https://cloud.oracle.com) (Compute Instance Always Free).
2. Abres el puerto `5000` en la lista de seguridad de la VCN.
3. Te conectas por SSH a la máquina, instalas python y ejecutas:
   ```bash
   nohup python3 servidor.py &
   ```
4. Ambos dispositivos usan `cliente_gui.py` apuntando directamente a la IP pública de tu VPS.
