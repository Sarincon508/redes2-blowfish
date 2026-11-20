# GUION TÉCNICO PARA VIDEO DE 2.5 MINUTOS (150 SEGUNDOS)
## Proyecto Integrador – Muestra del 30 de Mayo de 2025
### Aplicación de Mensajería Segura con Cifrado Blowfish (TCP / Capa de Aplicación)

---

### 📋 FICHA DE ENTREGA (Para el informe IEEE y descripción del video)
- **Título del Proyecto:** Mensajería Segura con Cifrado Simétrico Blowfish en Arquitectura Cliente-Servidor TCP.
- **Evento / Fecha:** Muestra de Proyectos Integradores – 30 de Mayo de 2025.
- **Asignatura Eje:** Redes II (con articulación interdisciplinar).
- **Enlace al Video (YouTube / Drive):** `https://youtu.be/TU_ENLACE_AQUI` *(Insertar en el informe IEEE)*.
- **Repositorio de Código:** `https://github.com/Sarincon508/redes2-blowfish.git`

---

## ⏱️ CRONOGRAMA EXACTO SEGUNDO A SEGUNDO (Total: 02:30 min)

| Intervalo | Tiempo | Bloque | Qué mostrar en Pantalla | Voz / Parlamentos |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:25** | 25 seg | **1. Introducción y Contexto** | Portada con título del proyecto, integrantes, fecha (30 de mayo de 2025) y cámara. | Saludo, presentación del equipo y problema que resuelve (datos en texto plano en la red). |
| **00:25 - 00:55** | 30 seg | **2. Articulación por Asignaturas** | Diapositiva esquemática con los 3 pilares / asignaturas del semestre. | Explicación concreta del aporte de cada materia al proyecto. |
| **00:55 - 02:05** | 70 seg | **3. Demostración en Vivo y Logs de Cifrado** | **Pantalla dividida:** Cliente emisor + Consola del Servidor (`servidor.py`) con logs en HEX + Cliente receptor. | Envío del mensaje, visualización de los logs en crudo (IV + HEX cifrado) y validación de descifrado. |
| **02:05 - 02:30** | 25 seg | **4. Conclusión y Cierre** | Diapositiva de métricas y cierre con enlace a GitHub y agradecimientos. | Conclusiones sobre confidencialidad en tránsito y despedida. |

---

## 🎙️ GUION PASO A PASO CON PARLAMENTOS

---

### 🕒 [00:00 – 00:25] BLOQUE 1: INTRODUCCIÓN Y CONTEXTO
**En Pantalla:** 
Diapositiva inicial con el membrete institucional, título del proyecto: *"Mensajería Segura con Cifrado Blowfish"*, nombres de los integrantes y referencia a la **Muestra de Proyectos Integradores del 30 de Mayo de 2025**.

> **Voz (Expositor 1):**  
> *"Cordial saludo, docentes y compañeros. Presentamos la sustentación de nuestro Proyecto Integrador para la muestra del 30 de mayo de 2025.*  
> *Nuestro proyecto consiste en una aplicación cliente-servidor de mensajería en tiempo real diseñada para solventar la vulnerabilidad de intercepción de tráfico en texto plano en redes no seguras, implementando cifrado simétrico Blowfish en la capa de aplicación."*

---

### 🕒 [00:25 – 00:55] BLOQUE 2: APORTE A CADA ASIGNATURA
**En Pantalla:** 
Esquema visual que conecta las tres áreas del conocimiento con iconos o cajas claras:

```
[Redes II]               --> Sockets TCP (0.0.0.0:5000), Modelo TCP/IP, prevención de Sniffing.
[Seguridad Informática]  --> Criptografía simétrica Blowfish CBC 128-bit, IV de 64-bit y PKCS#7.
[Sistemas Distribuidos]  --> Arquitectura Cliente-Servidor multihilo en Python y serialización segura.
```

> **Voz (Expositor 2 o 1):**  
> *"Este proyecto articula directamente las competencias de nuestras asignaturas:*  
> 1. ***Redes II:*** *Implementamos sockets TCP concurrentes en la capa de transporte, analizando el flujo de paquetes y demostrando cómo proteger la carga útil frente a capturas maliciosas con Wireshark.*  
> 2. ***Seguridad Informática y Criptografía:*** *Integramos el algoritmo simétrico Blowfish con clave de 128 bits en modo CBC y vectores de inicialización dinámicos de 64 bits, garantizando estricta confidencialidad.*  
> 3. ***Sistemas Distribuidos / Programación Concurrente:*** *Estructuramos un backend multihilo en Python capaz de retransmitir paquetes a múltiples clientes concurrentes manteniendo baja latencia."*

---

### 🕒 [00:55 – 02:05] BLOQUE 3: DEMOSTRACIÓN PRÁCTICA Y LOGS DEL MENSAJE CIFRADO *(¡Momento clave!)*
**En Pantalla:**
Organiza la pantalla en 3 partes visibles:
1. **Izquierda:** `cliente_gui.py` (Usuario: "Estudiante A").
2. **Centro (Grande):** Consola del Servidor (`servidor.py`) corriendo y esperando tráfico.
3. **Derecha:** `cliente_gui.py` o segundo cliente (Usuario: "Estudiante B").

*(Acción en pantalla: El Estudiante A escribe: `Mensaje Confidencial Muestra 30 Mayo` y da clic en "Enviar")*

> **Voz (Expositor 3 o quien demuestre):**  
> *"Pasemos a la demostración práctica en vivo y a la inspección de los logs del sistema.*  
> *En la izquierda, el emisor escribe el mensaje: 'Mensaje Confidencial Muestra 30 Mayo'. Al enviarlo, el cliente aplica el relleno PKCS#7, genera un IV aleatorio de 8 bytes y cifra el paquete con Blowfish."*

*(Acción en pantalla: Hacer zoom o resaltar con el puntero la consola del Servidor donde salta el log):*

```text
=================================================================
[PAQUETE DE RED RECIBIDO] Dispositivo: 192.168.1.15:52341
Tamano del payload TCP: 48 bytes
Cuerpo cifrado (HEX): 4f8b2d19e07ca31f9b34...c508a1
[CONTENIDO DESCIFRADO CON CLAVE]: Estudiante A: Mensaje Confidencial Muestra 30 Mayo
=================================================================
```

> **Voz:**  
> *"Observemos aquí la consola del servidor y el monitor de red:  
> Como pueden apreciar en los logs, el socket TCP recibe un payload crudo de 48 bytes. En tránsito por la red NO viaja texto legible, sino este vector hexadecimal indescifrable (`Cuerpo cifrado HEX`).*  
> *Cualquier atacante que intercepte el canal solo verá ruido criptográfico. Únicamente los nodos que poseen la clave simétrica compartida logran descifrar y reconstruir el mensaje original, tal como vemos que lo recibe el cliente receptor a la derecha."*

---

### 🕒 [02:05 – 02:30] BLOQUE 4: CONCLUSIÓN Y CIERRE
**En Pantalla:** 
Diapositiva final con conclusiones del proyecto, enlace visible al repositorio de GitHub (`https://github.com/Sarincon508/redes2-blowfish`) y agradecimientos.

> **Voz (Expositor 1 / Todos):**  
> *"En conclusión, comprobamos que el cifrado en la capa de aplicación con Blowfish proporciona una protección robusta y ligera, con un tiempo de procesamiento inferior a 10 milisegundos por paquete, haciéndolo ideal para entornos de comunicación distribuida en tiempo real.*  
> *El informe en formato IEEE, el código fuente y las pruebas están disponibles en el repositorio. Muchas gracias por su atención."*

---

## 📌 GUÍA RÁPIDA: CÓMO REPRODUCIR LOS LOGS PARA LA GRABACIÓN

Para grabar la pantalla y capturar los logs en vivo exactamente como pide el guion:

1. **Abrir Terminal 1 (Servidor):**
   ```powershell
   python servidor.py
   ```
2. **Abrir Terminal 2 (Cliente 1):**
   ```powershell
   python cliente_gui.py
   ```
   *(Ingresar nombre "Emisor" e IP `127.0.0.1`)*
3. **Abrir Terminal 3 (Cliente 2):**
   ```powershell
   python cliente_gui.py
   ```
   *(Ingresar nombre "Receptor" e IP `127.0.0.1`)*
4. Enviar el mensaje desde el Cliente 1 y enfocar la terminal del **Servidor**, donde se imprimirán los bloques:
   - `[PAQUETE DE RED RECIBIDO]`
   - `Tamano del payload TCP: XX bytes`
   - `Cuerpo cifrado (HEX): ...`
