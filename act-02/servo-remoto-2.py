import math
import time
import requests
import RPi.GPIO as GPIO

# Configuración de pines físicos
SERVO_PIN = 18 # BCM 18: pin físico 12
INDICADOR_PIN = 23 # BCM 23: pin físico 16

# Inicialización de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Añadido para evitar advertencias como en los scripts de prueba
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(INDICADOR_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50) # PWM a 50 Hz
pwm.start(0)

# Direcciones URL (asignación directa de IPs sin usar input)
url_servo = "http://192.168.4.126:8080"
url_indicador = "http://192.168.4.206:8080"

# Aumentamos el timeout basándonos en act1.py para evitar cortes por red WiFi
TIMEOUT_PETICION = 20.0 

def obtener_datos(base_url, parametros):
    try:
        # Se usa el nuevo timeout tolerante a alta latencia
        respuesta = requests.get(base_url + "/get?" + parametros, timeout=TIMEOUT_PETICION) 
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos
    except Exception as error:
        # Si falla, imprimimos el error de forma silenciada o lo dejamos pasar
        return None

def calcular_pwm(angulo):
    # Fórmula ajustada basada en servo-90.py y servo-180.py
    # 0° = 2.5 | 90° = 7.5 | 180° = 12.5
    duty = 2.5 + (angulo / 180.0) * 10.0
    return duty

tiempo_ultima_lectura_servo = time.monotonic()
tiempo_ultima_lectura_indicador = time.monotonic()

try:
    print("Iniciando control. Presiona Ctrl+C para detener.")
    while True:
        # 1. Control del Servomotor (Teléfono 1: .126)
        datos_servo = obtener_datos(url_servo, "accX&accY&accZ")
        if datos_servo and "buffer" in datos_servo:
            try:
                ax = datos_servo["buffer"]["accX"]["buffer"][-1]
                ay = datos_servo["buffer"]["accY"]["buffer"][-1]
                az = datos_servo["buffer"]["accZ"]["buffer"][-1]
                
                # Estimar inclinación
                theta = math.atan2(ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
                
                # Limitar a rango -45° a 45° y mapear a 45° a 135°
                theta = max(-45, min(45, theta))
                phi = theta + 90
                
                pwm.ChangeDutyCycle(calcular_pwm(phi))
                tiempo_ultima_lectura_servo = time.monotonic() # Refrescar tiempo tras éxito
            except (KeyError, IndexError):
                pass
                
        # 2. Control del Indicador (Teléfono 2: .106)
        datos_ind = obtener_datos(url_indicador, "linX&linY&linZ")
        if datos_ind and "buffer" in datos_ind:
            try:
                lx = datos_ind["buffer"]["linX"]["buffer"][-1]
                ly = datos_ind["buffer"]["linY"]["buffer"][-1]
                lz = datos_ind["buffer"]["linZ"]["buffer"][-1]
                
                # Calcular magnitud de aceleración lineal
                a_lin = math.sqrt(lx**2 + ly**2 + lz**2)
                
                # Criterio de activación > 15 m/s^2
                if a_lin > 15:
                    GPIO.output(INDICADOR_PIN, GPIO.HIGH)
                else:
                    GPIO.output(INDICADOR_PIN, GPIO.LOW)
                tiempo_ultima_lectura_indicador = time.monotonic() # Refrescar tiempo tras éxito
            except (KeyError, IndexError):
                pass
                
        # 3. Detección de fallas 
        # Ahora el margen de error respeta los 20 segundos del timeout (20 + 2 segundos extra)
        if (time.monotonic() - tiempo_ultima_lectura_servo) > (TIMEOUT_PETICION + 2.0):
            print("Falla extendida con Teléfono 1 (Servo). Suspendiendo señal PWM.")
            pwm.ChangeDutyCycle(0) 
            
        if (time.monotonic() - tiempo_ultima_lectura_indicador) > (TIMEOUT_PETICION + 2.0):
            print("Falla extendida con Teléfono 2 (Indicador). Apagando indicador.")
            GPIO.output(INDICADOR_PIN, GPIO.LOW) 

        time.sleep(0.1) 

except KeyboardInterrupt:
    print("Finalizando ejecución...")
finally:
    # Apagar el indicador, detener PWM y liberar los GPIO
    GPIO.output(INDICADOR_PIN, GPIO.LOW)
    pwm.stop()
    GPIO.cleanup()
