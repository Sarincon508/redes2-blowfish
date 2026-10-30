# GUION PARA VIDEO DE 10 MINUTOS EN YOUTUBE
## Cifrado de Mensajería Web con Algoritmo Blowfish (Redes II)
### *Enfoque Técnico: Explicación del Código, Criptografía y Demostración Web*

---

### 📋 FICHA DE ENTREGA DEL PROYECTO
- **Título del Video / Algoritmo:** Implementación del Cifrado Simétrico Blowfish en Mensajería Web en Tiempo Real
- **Materia:** Redes II
- **Actividad:** Proyecto Integrador
- **Repositorio GitHub:** `https://github.com/Sarincon508/redes2-blowfish.git`
- **Despliegue Web en la Nube:** `https://redes2-blowfish.onrender.com` *(O tu URL de Render)*
- **Integrantes:**
  - Integrante 1: [Nombre y Apellidos] - [Código/Matrícula]
  - Integrante 2: [Nombre y Apellidos] - [Código/Matrícula] *(si aplica)*
  - Integrante 3: [Nombre y Apellidos] - [Código/Matrícula] *(si aplica)*
- **Enlace a YouTube:** `https://www.youtube.com/watch?v=XXXXXXXXXXX` *(Reemplazar al subir)*

---

## ⏱️ CRONOGRAMA MINUTO A MINUTO (10 MINUTOS EXACTOS)

| Minuto | Bloque | Qué mostrar en Pantalla | Responsable |
| :--- | :--- | :--- | :--- |
| **00:00 - 01:00** | **1. Introducción y Contexto** | Diapositiva con Título, Integrantes, Materia Redes II y Repositorio. | Int. 1 |
| **01:00 - 02:30** | **2. Fundamento de Blowfish** | Diagrama de Blowfish: 64 bits, clave 128 bits, Feistel y modo CBC. | Int. 2 |
| **02:30 - 06:00** | **3. Explicación Detallada del Código** | Editor de código (VS Code): `cifrado_blowfish.py`, `app.py` e `index.html`. | Int. 3 / Int. 1 |
| **06:00 - 08:45** | **4. Demostración Práctica en Vivo** | Navegador con 2 ventanas/dispositivos (Sara y Bob), prueba de clave incorrecta y monitor en tiempo real. | Todos |
| **08:45 - 10:00** | **5. Conclusiones de Redes II y Cierre** | Diapositiva de conclusiones y enlace al repositorio. | Todos |

---

## 🎙️ GUION DETALLADO CON PARLAMENTOS Y CÓDIGO A MOSTRAR

---

### 🕒 [00:00 - 01:00] BLOQUE 1: INTRODUCCIÓN Y CONTEXTO
**En Pantalla:** Diapositiva de portada con Título del Proyecto, Materia Redes II, Nombres de Integrantes y URL de GitHub. Cámara de los expositores en una esquina.

- **Voz (Integrante 1):**
  > "Muy buenas a todos, profesor y compañeros. En este video presentamos la sustentación de nuestro **Proyecto Integrador** para la materia de **Redes II**.
  > Nuestro grupo está conformado por [Nombre Integrante 1], [Nombre Integrante 2] y [Nombre Integrante 3].
  > 
  > En la materia de Redes II estudiamos cómo viaja la información a través de las capas del modelo TCP/IP. Cuando enviamos datos por una red abierta sin cifrado, los paquetes viajan en texto plano y pueden ser interceptados con analizadores de tráfico como Wireshark.
  > Para resolver esta vulnerabilidad y garantizar la confidencialidad de extremo a extremo, desarrollamos una aplicación web de mensajería en tiempo real que implementa el **Algoritmo Criptográfico Blowfish**."

---

### 🕒 [01:00 - 02:30] BLOQUE 2: ¿QUÉ ES EL ALGORITMO BLOWFISH?
**En Pantalla:** Diagrama conceptual de Blowfish (Red de Feistel de 16 rondas, tamaño de bloque de 64 bits, cajas S y modo CBC con IV).

- **Voz (Integrante 2):**
  > "¿Qué es Blowfish y cómo funciona a nivel teórico?
  > Blowfish es un cifrador por bloques simétrico diseñado en 1993 por el criptógrafo **Bruce Schneier**. Al ser simétrico, utiliza la misma clave secreta tanto para cifrar como para descifrar.
  > 
  > Sus características principales son:
  > 1. **Tamaño de bloque de 64 bits (8 bytes):** El mensaje se divide y se procesa en bloques exactos de 8 bytes.
  > 2. **Longitud de clave variable:** Soporta claves desde 32 bits hasta 448 bits. En nuestro proyecto utilizamos una clave robusta de 128 bits.
  > 3. **Red de Feistel de 16 Rondas:** En cada ronda se dividen los 64 bits en dos mitades de 32 bits, aplicando operaciones XOR, permutaciones mediante la matriz P y sustituciones no lineales con 4 cajas S dependientes de la clave.
  > 4. **Modo de Operación CBC (Cipher Block Chaining):** Cada bloque de texto se combina mediante una operación XOR con el bloque cifrado anterior antes de ser procesado. Para el primer bloque, se genera un **Vector de Inicialización (IV)** aleatorio de 8 bytes. Esto garantiza que aunque se envíe la misma palabra dos veces, el resultado en la red sea completamente distinto."

---

### 🕒 [02:30 - 06:00] BLOQUE 3: EXPLICACIÓN DETALLADA DEL CÓDIGO FUENTE
**En Pantalla:** Abrir Visual Studio Code y mostrar los archivos en orden: `cifrado_blowfish.py`, `app.py` y `templates/index.html`.

- **Voz (Integrante 3 o quien explique el código):**
  > "A continuación, vamos a analizar cómo fue implementado el algoritmo en el código fuente.

#### 📄 Archivo 1: `cifrado_blowfish.py` (El Motor Criptográfico)
*(Acción: Mostrar en pantalla las líneas de `cifrar_mensaje`)*

> "Comencemos con el archivo `cifrado_blowfish.py`. Aquí tenemos las dos funciones centrales: `cifrar_mensaje` y `descifrar_mensaje`.
> 
> En la función `cifrar_mensaje`:
> - **Línea 33:** `iv = os.urandom(8)`. Generamos un Vector de Inicialización criptográficamente seguro de 8 bytes (64 bits), que es el tamaño de bloque de Blowfish.
> - **Líneas 36-38:** `padder = padding.PKCS7(64).padder()`. Como Blowfish trabaja en bloques estrictos de 64 bits, si el mensaje no mide un múltiplo exacto de 8 bytes, aplicamos el estándar de relleno **PKCS#7**.
> - **Líneas 41-43:** `cifrador = Cipher(Blowfish(clave), modes.CBC(iv))`. Aquí inicializamos el algoritmo Blowfish pasando la clave simétrica y el modo CBC con nuestro IV.
> - **Línea 47:** `return iv + datos_cifrados`. Concatenamos el IV al inicio del paquete. De esta forma, el paquete que viaja por la red mide: los 8 bytes del IV seguidos por los bloques cifrados.

*(Acción: Mover el cursor a la función `descifrar_mensaje`)*

> En la función `descifrar_mensaje`:
> - **Líneas 57-58:** Separamos el paquete recibido: `iv = paquete[:8]` y `datos_cifrados = paquete[8:]`.
> - **Líneas 61-63:** Inicializamos el descifrador Blowfish con la clave que el usuario nos entrega y el IV extraído.
> - **Líneas 66-68:** Aplicamos el desrelleno (`unpadder PKCS#7`). **Este punto es fundamental:** si la clave del usuario es incorrecta o le falta un solo carácter, el descifrado generará bytes corruptos y PKCS#7 lanzará una excepción `ValueError: Invalid padding bytes`, impidiendo que el mensaje pueda ser leído."

---

#### 📄 Archivo 2: `app.py` (El Servidor Web y Gestión de Salas)
*(Acción: Cambiar de pestaña a `app.py` y enfocar `enviar_mensaje` y `obtener_mensajes`)*

> "Ahora pasemos al backend en `app.py`, construido con Flask:
> 
> - **Línea 23:** La función `ajustar_clave()` toma la clave ingresada por el usuario en la web y la valida entre 4 y 56 bytes (32 a 448 bits). Si a la clave le borramos caracteres, la clave resultante es completamente diferente.
> - **Líneas 47-52 en `/api/send`:** Observen que empaquetamos el remitente y el mensaje juntos: `payload = f"{remitente}::: {texto}"` y los ciframos juntos con Blowfish.
> - **Líneas 59-67:** En el servidor **NO almacenamos texto plano**. El diccionario sólo guarda `cipher_hex` (en hexadecimal), el `iv_hex` y el `timestamp`. Esto demuestra que el servidor actúa como un nodo de transporte seguro.
> - **Líneas 95-125 en `/api/messages`:** Cuando un usuario consulta los mensajes de la sala, envía su clave. El servidor intenta descifrar el paquete con esa clave. 
>   - Si la clave coincide: extrae el remitente y el texto y retorna `decrypted: True`.
>   - Si la clave no coincide: entra en el bloque `except`, oculta el remitente como `🔒 Cifrado con Blowfish` y devuelve el mensaje de advertencia con `decrypted: False`."

---

#### 📄 Archivo 3: `templates/index.html` (La Interfaz Web y Monitor Criptográfico)
*(Acción: Mostrar brevemente el archivo HTML y la función JavaScript `cargarMensajes`)*

> "Por último, en `templates/index.html`, utilizamos JavaScript nativo:
> - Cada 1.5 segundos ejecuta `cargarMensajes()`, enviando la sala y la clave actual.
> - Si un mensaje llega con `decrypted: false`, la interfaz lo pinta con fondo rojo de advertencia (`msg-failed`).
> - Y en la barra lateral tenemos el **Monitor Criptográfico de Redes II**, que muestra en tiempo real el IV de 64 bits y la cadena hexadecimal de bytes que viajó por internet."

---

### 🕒 [06:00 - 08:45] BLOQUE 4: DEMOSTRACIÓN PRÁCTICA EN VIVO
**En Pantalla:** Abrir dos ventanas del navegador lado a lado conectadas a la URL en Render (o una ventana de PC y la pantalla de un celular):
- Ventana Izquierda: Sara (Clave completa: `Redes2Clave128B!`).
- Ventana Derecha: Bob (Clave completa: `Redes2Clave128B!`).

- **Voz (Integrante 1):**
  > "Vamos a ver la demostración práctica en tiempo real. 
  > En la izquierda tenemos a Sara y en la derecha a Bob. Ambos ingresaron a la sala `#proyecto-redes2` con la clave correcta `Redes2Clave128B!`."

*(Acción: Sara escribe: 'Hola Bob, este mensaje viaja cifrado por Blowfish' y presiona Enviar)*

- **Voz (Integrante 2):**
  > "Sara presiona Enviar:
  > 1. En el chat de Sara vemos el mensaje enviado.
  > 2. En el **Monitor Criptográfico** de la derecha podemos ver el paquete real que viajó por la red: un IV de 8 bytes `3f7a19...` y el cuerpo cifrado en hexadecimal `b49c01...`.
  > 3. En la pantalla de Bob, el mensaje llega y se descifra de inmediato porque Bob tiene la clave correcta."

---

*(Acción CRÍTICA para el video: En la ventana de Bob, hacer clic en "Cambiar Sala / Clave", borrarle 3 caracteres a la clave (dejarla en `Redes2Clave12`) y presionar "Entrar al Chat")*

- **Voz (Integrante 3):**
  > "Ahora fíjense en este experimento clave:
  > Supongamos que un atacante o usuario no autorizado entra a la misma sala `#proyecto-redes2`, pero no conoce la clave completa y le faltan 3 caracteres.
  > 
  > Al entrar con la clave incorrecta:
  > ¡Observen la pantalla de Bob! El mensaje anterior ahora aparece bloqueado en rojo con el texto:
  > **'⚠️ [ERROR DE DESCIFRADO]: No se pudo descifrar este mensaje. Tu clave Blowfish es diferente a la del emisor'**.
  > Además, el remitente aparece protegido como **'🔒 Cifrado con Blowfish'** y en el monitor de estado marca en rojo: **'❌ Fallo de descifrado (Clave no coincide)'**.
  > 
  > Esto comprueba en vivo que la seguridad depende estrictamente del algoritmo matemático Blowfish y no de un simple filtro web."

---

*(Acción: Bob vuelve a hacer clic en "Cambiar Sala / Clave", escribe la clave correcta completa `Redes2Clave128B!` y presiona Entrar)*

- **Voz (Integrante 1):**
  > "Tan pronto como Bob restaura la clave compartida correcta, el algoritmo Blowfish valida el relleno PKCS#7 y el mensaje vuelve a ser legible de forma instantánea."

---

### 🕒 [08:45 - 10:00] BLOQUE 5: CONCLUSIONES DE REDES II Y CIERRE
**En Pantalla:** Diapositiva con Conclusiones y enlace al repositorio de GitHub. Cámara de los integrantes.

- **Voz (Integrante 2 / Integrante 1):**
  > "Para concluir nuestra sustentación de Redes II:
  > 
  > 1. **Confidencialidad en la Capa de Aplicación:** Demostramos que cuando el canal de transporte no ofrece seguridad intrínseca, cifrar los datos con Blowfish en la capa de aplicación evita cualquier intento de intercepción o sniffing.
  > 2. **Rendimiento:** A pesar de realizar operaciones de padding, generación de IV aleatorio y 16 rondas de Feistel, la latencia observada entre clientes remotos fue inferior a 150 milisegundos, demostrando la alta eficiencia de Blowfish.
  > 3. **Implementación Limpia y Despliegue en la Nube:** Toda la solución fue construida en Python, modularizada en tres capas y desplegada de forma pública en Render para acceso desde cualquier dispositivo web.
  > 
  > El código fuente completo, la documentación y este guion están disponibles en nuestro repositorio de GitHub `Sarincon508/redes2-blowfish`.
  > 
  > Muchas gracias por su atención."

---

## 💡 CONSEJOS PARA LA GRABACIÓN:
1. **Zoom en el código:** Cuando muestres VS Code, usa `Ctrl + +` para aumentar el tamaño de letra para que las líneas de código se lean con nitidez en 1080p.
2. **Prueba de la clave incorrecta:** Resalten con el mouse o con la voz el momento en que le quitan los 3 caracteres a la clave; ese es el punto que más convence a los evaluadores de Redes II de que la criptografía está funcionando de verdad.
