# GUION PARA VIDEO DE 10 MINUTOS EN YOUTUBE
## Cifrado de Mensajería Web con Algoritmo Blowfish (Redes II)

---

### 📋 FICHA DE ENTREGA DEL PROYECTO
- **Título del Video / Algoritmo:** Cifrado Simétrico Blowfish aplicado a Mensajería Web en Tiempo Real con Arquitectura Cliente-Servidor
- **Materia:** Redes II
- **Actividad:** Proyecto Integrador
- **Repositorio GitHub:** `https://github.com/Sarincon508/redes2-blowfish.git`
- **Despliegue Web en la Nube:** `https://redes2-blowfish.onrender.com` *(Reemplazar con su URL de Render)*
- **Integrantes:**
  - Integrante 1: [Nombre y Apellidos] - [Código/Matrícula]
  - Integrante 2: [Nombre y Apellidos] - [Código/Matrícula] *(si aplica)*
  - Integrante 3: [Nombre y Apellidos] - [Código/Matrícula] *(si aplica)*
- **Enlace a YouTube:** `https://www.youtube.com/watch?v=XXXXXXXXXXX` *(Reemplazar al subir)*

---

## ⏱️ DISTRIBUCIÓN DEL TIEMPO (CRONOGRAMA DE 10 MINUTOS)

| Minuto | Sección | Contenido a Exponer |
| :--- | :--- | :--- |
| **00:00 - 01:15** | Introducción y Contexto de Redes II | Saludo, presentación de integrantes, mención del **Proyecto Integrador** y la materia de **Redes II** (vulnerabilidad de texto plano en redes y necesidad de confidencialidad). |
| **01:15 - 03:30** | Teoría y Funcionamiento de Blowfish | Cifrador simétrico de bloques de **64 bits**, clave de 128 bits, **Red de Feistel de 16 rondas**, modo **CBC** y vector de inicialización (**IV**). |
| **03:30 - 05:45** | Arquitectura Web e Implementación | Explicación del servidor Flask ([`app.py`](file:///F:/Users/Max/Desktop/redes/app.py)), el motor criptográfico ([`cifrado_blowfish.py`](file:///F:/Users/Max/Desktop/redes/cifrado_blowfish.py)) y la separación por salas privadas para mensajería 1 a 1. |
| **05:45 - 08:30** | Demostración en Vivo (100% Web) | Dos personas en ubicaciones distintas abriendo la página web desde sus navegadores/celulares, entrando a la misma sala privada, enviando mensajes y mostrando el monitor criptográfico. |
| **08:30 - 10:00** | Conclusiones y Cierre | Ventajas de Blowfish en rendimiento de red, análisis de seguridad frente a sniffing y despedida. |

---

## 🎙️ GUION MINUTO A MINUTO CON DIÁLOGOS

### 🕒 [00:00 - 01:15] BLOQUE 1: INTRODUCCIÓN Y CONTEXTO
**Pantalla:** Diapositiva de portada con Título, Repositorio GitHub, Materia "Redes II", Nombres de los Integrantes y enlace al despliegue web.

- **Voz (Integrante 1):**
  > "Muy buenas a todos, profesor y compañeros. En este video presentamos el desarrollo de nuestro **Proyecto Integrador** para la materia de **Redes II**.
  > Nuestro equipo está integrado por [Nombre Integrante 1], [Nombre Integrante 2] y [Nombre Integrante 3].
  > 
  > En Redes II analizamos cómo viajan los paquetes a través de los protocolos de transporte y aplicación. En un entorno real, los canales abiertos transmiten texto plano que puede ser capturado por interceptores.
  > Para resolver esto, hemos implementado una aplicación web de mensajería en tiempo real 100% accesible desde cualquier navegador o teléfono móvil, que protege toda la comunicación mediante el **Algoritmo de Cifrado Simétrico Blowfish**."

---

### 🕒 [01:15 - 03:30] BLOQUE 2: ¿QUÉ ES EL ALGORITMO BLOWFISH?
**Pantalla:** Diagrama de bloques de Blowfish, Red de Feistel (16 rondas), cajas S, cajas P y modo CBC.

- **Voz (Integrante 2 o Integrante 1):**
  > "Blowfish es un cifrador por bloques de clave simétrica diseñado por **Bruce Schneier** en 1993.
  > Sus características técnicas esenciales son:
  > 1. **Cifrado Simétrico:** Se comparte una clave secreta (en nuestro caso de 128 bits) tanto para cifrar como para descifrar.
  > 2. **Bloques de 64 bits (8 bytes):** Los datos se procesan en bloques de este tamaño exacto.
  > 3. **Red de Feistel con 16 Rondas:** Utiliza operaciones de sustitución con 4 cajas S y permutación con cajas P que transforman el texto plano en secuencias pseudoaleatorias.
  > 4. **Modo CBC (Cipher Block Chaining):** Empleamos un Vector de Inicialización (IV) de 8 bytes aleatorios por cada mensaje. Esto asegura que si se envía el mismo mensaje varias veces, el paquete que viaja por la red sea totalmente diferente, impidiendo ataques de repetición o análisis de frecuencias."

---

### 🕒 [03:30 - 05:45] BLOQUE 3: CÓMO SE IMPLEMENTÓ (ARQUITECTURA WEB)
**Pantalla:** Mostrar el repositorio GitHub `Sarincon508/redes2-blowfish` y el código fuente.

- **Voz (Integrante 3 o Integrante 2):**
  > "Para lograr que cualquier persona pueda usarlo sin instalar ningún programa en su computador, diseñamos una arquitectura web con Python y Flask:
  > 
  > 1. **Motor Criptográfico (`cifrado_blowfish.py`):**
  >    - Aplica relleno PKCS#7 al mensaje para alinearlo a múltiplos de 64 bits.
  >    - Genera el IV aleatorio y cifra con Blowfish en modo CBC.
  > 2. **Backend Web (`app.py`):**
  >    - Administra salas privadas mediante códigos compartidos. Esto permite que dos personas en lugares remotos entren a una sala exclusiva y sólo ellas puedan comunicarse.
  >    - Expone endpoints REST para envío y recepción en tiempo real.
  > 3. **Interfaz Web Adaptativa (`templates/index.html`):**
  >    - Diseñada con interfaz responsiva (apta para móviles y PCs) con un **Monitor Criptográfico** que inspecciona los bytes en hexadecimal del IV y del payload cifrado."

---

### 🕒 [05:45 - 08:30] BLOQUE 4: DEMOSTRACIÓN PRÁCTICA EN VIVO (2 DISPOSITIVOS / LUGARES DISTINTOS)
**Pantalla:** Grabar la pantalla dividida (o la pantalla de la PC y la pantalla de un celular conectado a la web):

- **Voz (Todos / Alternada):**
  > *(Acción: Persona 1 abre la URL en su navegador y escribe Nombre: 'Sara', Sala: 'redes-privada')*
  > **Int. 1:** "Estamos accediendo directamente desde la web. No hay programas locales corriendo. Sara entra a la sala privada llamada 'redes-privada'."
  > 
  > *(Acción: Persona 2 abre la URL desde su celular o segunda ventana y entra a 'redes-privada')*
  > **Int. 2:** "Al mismo tiempo, desde otra ubicación, el segundo integrante ingresa con su nombre a la misma sala privada."
  > 
  > *(Acción: Sara envía el mensaje: 'Hola, este mensaje está viajando seguro con Blowfish por internet')*
  > **Int. 3:** "Observen lo que sucede en tiempo real:
  > 1. El mensaje es cifrado al instante.
  > 2. En el **Monitor Criptográfico lateral** vemos el Vector de Inicialización (IV) de 8 bytes y el cuerpo cifrado en hexadecimal completo. Si un atacante intercepta la conexión HTTP/TCP, solo ve estos bytes ininteligibles.
  > 3. En la pantalla del segundo integrante, el mensaje aparece descifrado automáticamente en milisegundos."
  > 
  > *(Acción: El segundo integrante responde y se observa la actualización inmediata en el monitor)*

---

### 🕒 [08:30 - 10:00] BLOQUE 5: CONCLUSIONES Y CIERRE
**Pantalla:** Diapositiva de Conclusiones, métricas y agradecimientos.

- **Voz (Integrante 1 o cierre grupal):**
  > "Como conclusiones de este proyecto integrador:
  > 1. Logramos implementar exitosamente la confidencialidad en la capa de aplicación sin depender de software instalado en los clientes, operando 100% vía web.
  > 2. Comprobamos la velocidad y solidez del algoritmo Blowfish para aplicaciones interactivas en tiempo real.
  > 3. Todo el código fuente está disponible públicamente en nuestro repositorio de GitHub `Sarincon508/redes2-blowfish`.
  > 
  > Agradecemos al docente y a la materia de Redes II por los conocimientos adquiridos. ¡Muchas gracias!"
