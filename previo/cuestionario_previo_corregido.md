## Cuestionario Previo

Práctica 04

Alumno: Martin Quintero Rubio

Fecha de entrega: 26/octubre/2026

#### 1. ¿Qué se entiende por comunicación inalámbrica en un sistema embebido?

A la comunicación que usa como medio: ondas electromagnéticas, luz o sonido.

#### 2. Menciona al menos dos tecnologías de comunicación inalámbrica que conozcas y describe brevemente en qué tipo de aplicaciones se utilizan

1. Wi-Fi: Usa ondas de radio de $2.4[GHz]$, $5[GHz]$ y $6[GHz]$ y que cumplen con el estándar IEEE 802.11.

2. Bluetooth: Usa ondas de radio en la banda de $2.4[GHz]$ que cumplen con el estándar IEEE 802.15.1. 

#### 3. ¿Cuál es la diferencia entre comunicación cableada y una inalámbrica en términos de ventajas y desventajas?

La comunicación cableada usa cables para conectar el dispositivo a una red o con los demás dispositivos, mientras que la **inalámbrica** usa algún protocolo de comunicación por radio para comunicarse.

| Tipo conexión | Ventajas | Desventajas |
| --- | --- | --- |
| Cableada | Puede transportar corriente (PoE)<br>Muy estable<br>Alta velocidad | Los cables pueden estorbar<br>No siempre se puede cablear |
| No cableada | Facilidad de instalación<br>No requiere infraestructura previa, solo un AP o cliente Wireless (Wi-Fi/Bluetooth) | Baja velocidad<br>Propensa a interferencias |

#### 4. ¿Qué es una red Wi-Fi y qué elementos básicos la componen?

Una red Wi-Fi es una red de datos a la que pueden conectarse dispositivos inalámbricos. Su componente básico es el punto de acceso inalámbrico (AP).

Componentes básicos:
*   Punto de acceso inalámbrico: Es una antena que genera una señal de radio en el estándar 802.11 (Wi-Fi) o 802.15 (Bluetooth) con un nombre.
*   Clientes inalámbricos: Pueden ser teléfonos, computadoras, dispositivos IoT, impresoras, etc., que tienen la capacidad de identificar y conectarse a un punto de acceso.

Componentes opcionales:
*   Router: Puede ser alámbrico o inalámbrico y permite que la red Wi-Fi tenga conexión con otras redes.
*   Repetidores: Amplían el alcance de la red Wi-Fi.

#### 5. ¿Qué es el protocolo HTTP y en qué tipo de aplicaciones se utiliza?

Es un protocolo de aplicación del stack TCP/IP que se apoya de TCP y UDP en las versiones más recientes. Su propósito es proporcionar una forma sencilla de comunicar servidores y aplicaciones cliente para la transferencia de información más allá del texto o archivos. Proporciona métodos y códigos de estado para realizar esta comunicación.

Las aplicaciones que más usan HTTP son los navegadores y servidores WEB; sin embargo, en la actualidad, casi todas las aplicaciones, tanto móviles como de escritorio, también usan HTTP debido a los métodos que proporciona y a la popularización del desarrollo de aplicaciones centradas en un backend. Es decir, un servidor que recibe las peticiones de distintas aplicaciones que usan la misma lógica de negocio.

#### 6. ¿Qué es una petición (Request) y qué es una respuesta (Response) en el contexto de HTTP?

Una petición es una solicitud de un recurso del servidor que realiza un cliente usando un método HTTP, por ejemplo GET:

```http
GET /index.html HTTP/1.1
Host: ejemplo.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0
Accept: text/html,application/xhtml+xml
Accept-Language: es-ES,es;q=0.9
```

Mientras que una respuesta es el recurso y los mensajes que devuelve el servidor HTTP al cliente; para este ejemplo:

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 124

<!DOCTYPE html>
<html>
<head><title>Página de Ejemplo</title></head>
<body><h1>¡Hola, mundo!</h1></body>
</html>
```

#### 7. Explica brevemente el modelo cliente-servidor. ¿Cuál es el rol de cada uno?

Se trata de una arquitectura de desarrollo e implementación de soluciones en la que las tareas se dividen. Un servidor está siempre activo en el mismo lugar (dirección/dominio) a la espera de que los clientes se conecten y hagan uso de los servicios que este proporciona, que pueden ser servicios de red, de datos o de información.

#### 8. ¿Qué es una API y qué significa que un dispositivo exponga una API?

Una API (Application Programming Interface) es un conjunto de servicios que va a ofrecer un dispositivo o servidor, junto con las reglas y documentación necesarias para que los programadores o usuarios hagan uso de estas para construir sistemas más complejos. Por ejemplo, un banco puede exponer su API para transferencias masivas, la cual puede ser usada por un departamento de nóminas para dispersar de manera eficiente sus pagos a los trabajadores; o una cámara de videovigilancia puede exponer la forma adecuada de obtener el flujo secundario de video para hacer analítica.

#### 9. ¿Qué formato de datos es utilizado comúnmente en respuestas HTTP y por qué es útil?

El formato JSON (JavaScript Object Notation) es muy común debido a que ofrece un equilibrio entre ser fácil de entender por las personas y fácil de procesar por los sistemas, por lo que es el formato que más se usa actualmente por los sistemas y servidores para responder las peticiones de sus APIs.

#### 10. ¿Qué diferencia hay entre obtener datos de un sensor localmente y obtenerlos de un dispositivo remoto?

Principalmente el protocolo de comunicación. Si es local se podría usar I2C, SPI o UART; si es remoto, tal vez se tenga que usar protocolos del stack TCP/IP.