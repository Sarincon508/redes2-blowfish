# GUION PARA VIDEO DE 10 MINUTOS EN YOUTUBE
## Cifrado de Mensajería con Algoritmo Blowfish en Sockets TCP

---

### 📋 FICHA DE ENTREGA DEL PROYECTO
- **Título del Video / Algoritmo:** Cifrado Simétrico Blowfish aplicado a Mensajería en Tiempo Real con Sockets TCP
- **Materia:** Redes II
- **Actividad:** Proyecto Integrador
- **Integrantes:**
  - Integrante 1: [Nombre y Apellidos] - [Código/Matrícula]
  - Integrante 2: [Nombre y Apellidos] - [Código/Matrícula] *(si aplica)*
  - Integrante 3: [Nombre y Apellidos] - [Código/Matrícula] *(si aplica)*
- **Enlace a YouTube:** `https://www.youtube.com/watch?v=XXXXXXXXXXX` *(Reemplazar al subir)*

---

## ⏱️ DISTRIBUCIÓN DEL TIEMPO (CRONOGRAMA DE 10 MINUTOS)

| Minuto | Sección | Responsable sugerido |
| :--- | :--- | :--- |
| **00:00 - 01:15** | Introducción, Integrantes y Contexto de Redes II | Integrante 1 (o todos) |
| **01:15 - 03:30** | Teoría y Funcionamiento del Algoritmo Blowfish | Integrante 2 (o Int. 1) |
| **03:30 - 06:00** | Explicación del Código e Implementación Técnica | Integrante 3 (o Int. 2) |
| **06:00 - 08:30** | Demostración Práctica en Vivo (Sockets + Cifrado en 2 dispositivos) | Todos los integrantes |
| **08:30 - 10:00** | Importancia en Redes, Comparativa y Conclusiones | Integrante 1 (o todos) |

---

## 🎙️ GUION MINUTO A MINUTO CON DIÁLOGOS

### 🕒 [00:00 - 01:15] BLOQUE 1: INTRODUCCIÓN Y CONTEXTO
**Pantalla:** Diapositiva de portada con Título, Logos de la Universidad, Materia "Redes II", Nombres de los Integrantes y fecha. Cámara de los expositores activa.

- **Voz (Integrante 1):**
  > "Muy buenas a todos, profesor y compañeros. En este video presentamos el desarrollo de nuestro **Proyecto Integrador** para la materia de **Redes II**.
  > Nuestro equipo está integrado por [Nombre Integrante 1], [Nombre Integrante 2] y [Nombre Integrante 3].
  > 
  > En la materia de Redes II estudiamos cómo viajan los datos a través de los protocolos de transporte como TCP y cómo se interconectan los sistemas. Sin embargo, un canal de comunicación estándar transporta la información en texto plano, lo que representa una grave vulnerabilidad de seguridad ante ataques de intercepción o *sniffing*. 
  > Por ello, para este proyecto integrador hemos diseñado e implementado una aplicación de mensajería instantánea segura basada en sockets TCP utilizando el **Algoritmo de Cifrado Simétrico Blowfish**."

---

### 🕒 [01:15 - 03:30] BLOQUE 2: ¿QUÉ ES EL ALGORITMO BLOWFISH?
**Pantalla:** Diapositivas con diagramas de bloques de Blowfish, Red de Feistel (16 rondas), matriz S-Boxes y clave simétrica.

- **Voz (Integrante 2 o Integrante 1):**
  > "¿Qué es exactamente Blowfish y por qué lo elegimos?
  > Blowfish es un algoritmo de cifrado por bloques de clave simétrica, diseñado en 1993 por el reconocido criptógrafo **Bruce Schneier** como una alternativa pública, no patentada y mucho más rápida y segura que el antiguo estándar DES.
  > 
  > Sus características técnicas fundamentales son:
  > 1. **Cifrado Simétrico:** Ambos extremos (emisor y receptor) comparten la misma clave secreta para cifrar y descifrar la información.
  > 2. **Tamaño de Bloque de 64 bits (8 bytes):** Los mensajes se dividen y procesan en bloques exactos de 8 bytes.
  > 3. **Longitud de Clave Variable:** Acepta claves desde 32 bits hasta 448 bits. En nuestro caso utilizamos una clave robusta de 128 bits.
  > 4. **Estructura en Red de Feistel:** Utiliza 16 rondas iterativas de sustitución y permutación mediante matrices denominadas P-Boxes y 4 cajas de sustitución o S-Boxes dependientes de la clave.
  > 
  > Además, para nuestra implementación en Redes II utilizamos el modo de operación **CBC (Cipher Block Chaining)** con un **Vector de Inicialización (IV)** aleatorio de 8 bytes. Esto garantiza que aunque un usuario envíe dos veces la misma palabra (como 'Hola'), el resultado cifrado que viaja por los cables sea completamente diferente, impidiendo ataques de análisis de patrones."

---

### 🕒 [03:30 - 06:00] BLOQUE 3: CÓMO SE IMPLEMENTÓ (EXPLICACIÓN DEL CÓDIGO)
**Pantalla:** Editor de código (VS Code / Python) mostrando los 3 archivos: `cifrado_blowfish.py`, `servidor.py` y `cliente.py` / `cliente_gui.py`.

- **Voz (Integrante 3 o Integrante 2):**
  > "Veamos ahora la arquitectura del software. El proyecto está dividido de forma modular en tres componentes:
  > 
  > 1. **Módulo de Criptografía (`cifrado_blowfish.py`):**
  >    - Aquí definimos la función `cifrar_mensaje()`. Esta función toma el texto plano, genera un vector IV aleatorio con `os.urandom(8)`, aplica relleno o *padding* PKCS#7 para que el texto sea múltiplo exacto de 64 bits, y ejecuta el cifrado Blowfish en modo CBC. Al final, concatena el IV al inicio del paquete cifrado.
  >    - La función `descifrar_mensaje()` hace el proceso inverso: extrae los primeros 8 bytes como el IV, descifra el contenido restante con la clave simétrica y remueve el padding para recuperar el texto legible.
  > 
  > 2. **Servidor TCP Concurrente (`servidor.py`):**
  >    - Implementado con la librería nativa `socket` de Python en la capa de Transporte (TCP, puerto 5000), escuchando en `0.0.0.0` para admitir conexiones locales, de red Wi-Fi o remotas.
  >    - Utiliza hilos (`threading`) para admitir múltiples dispositivos simultáneos.
  >    - Lo más importante desde la perspectiva de Redes II: **el servidor recibe paquetes de bytes cifrados y los retransmite**. Si un atacante interceptara el servidor o los cables intermedios, sólo vería cadenas hexadecimales ilegibles.
  > 
  > 3. **Cliente de Mensajería (`cliente.py` / `cliente_gui.py`):**
  >    - Permite indicar la dirección IP del servidor para conectarse desde otra máquina o red.
  >    - Cuenta con dos hilos: uno para enviar mensajes cifrados y otro en segundo plano que escucha de forma continua los paquetes entrantes para descifrarlos en tiempo real."

---

### 🕒 [06:00 - 08:30] BLOQUE 4: DEMOSTRACIÓN PRÁCTICA EN VIVO (2 DISPOSITIVOS)
**Pantalla:** Demostración en vivo. Puede ser pantalla compartida o grabación donde se vea la PC Servidor y el Segundo Dispositivo conectado:

- **Voz (Todos / Alternada):**
  > *(Acción: En la PC 1 ejecutar `python servidor.py`)*
  > **Int. 1:** "Iniciamos el servidor en la PC principal. Vemos en pantalla que queda escuchando en el puerto 5000 y nos muestra la IP local de red Wi-Fi."
  > 
  > *(Acción: En la PC 1 abrir cliente Alicia, y en la PC 2 abrir cliente Bob conectándose a la IP de la PC 1)*
  > **Int. 2:** "Ahora conectamos el segundo dispositivo desde la red Wi-Fi ingresando la IP del servidor. Inmediatamente el servidor notifica la nueva conexión con su IP y puerto efímero."
  > 
  > *(Acción: Alicia escribe: 'Hola Bob, este mensaje viaja cifrado por Blowfish a través de la red')*
  > **Int. 3:** "Fíjense con mucha atención en lo que ocurre aquí:
  > Alicia escribe su mensaje en texto plano. En el momento en que presiona Enviar:
  > 1. En el monitor de red de Alicia vemos que el mensaje fue transformado en un arreglo de bytes hexadecimales.
  > 2. En la terminal del Servidor observamos el paquete que viajó por el socket TCP a través del router: `c48d7747991a87...`. Si alguien capturara los paquetes con Wireshark, no puede leer el texto original.
  > 3. En el segundo dispositivo, la ventana de Bob recibe esos bytes, utiliza la clave simétrica compartida y el IV para descifrar con Blowfish, y muestra en pantalla de inmediato: *'Alicia: Hola Bob, este mensaje viaja cifrado por Blowfish a través de la red'*."
  > 
  > *(Acción: Bob responde desde el segundo dispositivo: 'Recibido fuerte y claro con cifrado Blowfish')*
  > **Int. 1:** "Bob contesta y el proceso se repite en sentido inverso. La latencia es prácticamente nula porque Blowfish es un algoritmo sumamente veloz y optimizado para procesadores de 32 y 64 bits."

---

### 🕒 [08:30 - 10:00] BLOQUE 5: CONCLUSIONES Y CIERRE
**Pantalla:** Diapositiva de Conclusiones y Comparación (Blowfish vs otros algoritmos). Cámara de los integrantes.

- **Voz (Integrante 1 o cierre coordinado):**
  > "Para finalizar, queremos destacar los aprendizajes clave de este Proyecto Integrador de Redes II:
  > 
  > 1. **Seguridad Extremo a Extremo:** Demostramos que la seguridad en las redes no depende únicamente del canal físico, sino de la implementación de protocolos criptográficos en la capa de aplicación.
  > 2. **Rendimiento de Blowfish:** A pesar de haber sido creado en 1993, Blowfish ofrece una velocidad de procesamiento excelente en microprocesadores sin requerir aceleración de hardware compleja, siendo ideal para dispositivos embebidos o sistemas de telemetría de red.
  > 3. **Conexión con los estándares modernos:** Aunque Blowfish ha sido sucedido por Twofish y AES (debido a su tamaño de bloque de 64 bits frente a colisiones en volúmenes gigantescos de datos), sus principios de Red de Feistel y cajas S siguen siendo la base fundamental de la ciberseguridad en redes de computadoras.
  > 
  > Agradecemos al docente y a los compañeros por su atención. En la descripción del video dejamos el enlace al repositorio con todo el código fuente documentado. ¡Muchas gracias!"
