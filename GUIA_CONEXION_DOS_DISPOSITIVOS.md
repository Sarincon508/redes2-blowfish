# Guía: Cómo Conectar Dos Dispositivos Distintos al Servidor Blowfish
**Materia:** Redes II - Proyecto Integrador  

¡Sí es totalmente posible! De hecho, en **Redes II** hacer la prueba entre **dos dispositivos físicos distintos** (por ejemplo, dos laptops, o una PC de escritorio y una laptop) le dará un valor enorme a tu video de exposición.

Aquí tienes las 3 formas más prácticas y efectivas de lograrlo:

---

## 🌐 MÉTODO 1: En la misma red Wi-Fi o Red Local (LAN)
*(El método más fácil, recomendado y sin instalar nada extra)*

Ambos dispositivos deben estar conectados al mismo router o a la misma red Wi-Fi.

### Paso 1: Saber la IP de la computadora que será el Servidor
En la computadora donde vas a encender `servidor.py`, abre PowerShell y escribe:
```powershell
ipconfig
```
Busca donde dice **Dirección IPv4** (por ejemplo: `192.168.1.2` o `192.168.0.15`).

### Paso 2: Permitir el puerto en el Firewall de Windows (Sólo en la PC Servidor)
Por defecto, Windows bloquea conexiones entrantes de otras computadoras. Ejecuta este comando en PowerShell como **Administrador** en la PC Servidor:
```powershell
New-NetFirewallRule -DisplayName "Chat Redes II Blowfish" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```
*(O simplemente desactiva temporalmente el Firewall durante la grabación del video).*

### Paso 3: Iniciar el Servidor
En la PC 1 (Servidor), ejecuta:
```bash
python servidor.py
```
El servidor mostrará un mensaje indicando que está escuchando en el puerto 5000 y te recordará las IPs locales a usar.

### Paso 4: Conectar desde el Segundo Dispositivo (Laptop / PC 2)
Copia la carpeta del proyecto a la segunda computadora (o al menos `cliente.py`, `cliente_gui.py` y `cifrado_blowfish.py`).
Instala la librería criptográfica si no la tiene:
```bash
pip install cryptography
```
Ejecuta el cliente:
```bash
python cliente_gui.py
```
Cuando la ventana te pida la IP del Servidor:
- **No pongas 127.0.0.1**.
- Escribe la IP de la PC Servidor (por ejemplo: `192.168.1.2`).
- Presiona **Conectar**.

¡Listo! Ambos dispositivos estarán chateando en tiempo real con cifrado Blowfish a través del router Wi-Fi.

---

## 🌍 MÉTODO 2: Conexión por Internet usando Ngrok (Túnel TCP Gratuito)
*(Ideal si los integrantes del equipo están en casas diferentes)*

Si un integrante está en su casa y otro en la suya, no comparten la misma red Wi-Fi. La forma más rápida sin tener que configurar el módem de tu proveedor de internet es **Ngrok**:

1. Descarga **Ngrok** gratis desde [ngrok.com](https://ngrok.com).
2. En la PC del Servidor, abre una terminal y ejecuta:
   ```bash
   ngrok tcp 5000
   ```
3. Ngrok te dará una dirección pública similar a:
   `tcp://0.tcp.ngrok.io:14523`
4. En el segundo dispositivo, cuando el cliente pida la IP y el Puerto:
   - **IP / Host:** `0.tcp.ngrok.io`
   - **Puerto:** `14523`
5. Ambos estarán conectados por internet a través del túnel seguro.

---

## ☁️ MÉTODO 3: Desplegar en un Servidor en la Nube (VPS)
*(Nivel profesional)*

Si tienes una máquina virtual en la nube (AWS EC2, Google Cloud Compute Engine, Oracle Cloud Always Free, o DigitalOcean con Ubuntu/Debian):

1. Sube los archivos al VPS:
   ```bash
   scp servidor.py cifrado_blowfish.py usuario@IP_PUBLICA_VPS:/home/usuario/
   ```
2. Entra por SSH al VPS y ejecuta el servidor con `nohup` o `tmux`:
   ```bash
   python3 -m pip install cryptography
   python3 servidor.py
   ```
3. Asegúrate de abrir el puerto **5000/TCP** en el grupo de seguridad (Security Groups / Firewall) de tu proveedor cloud.
4. Ahora, cualquier dispositivo desde cualquier parte del mundo sólo tiene que abrir `cliente_gui.py`, escribir la **IP Pública del VPS** y comenzar a chatear.
