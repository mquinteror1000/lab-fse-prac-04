import math
import time
import requests
import RPi.GPIO as GPIO

# Configuración de pines físicos
SERVO_PIN = 18 # BCM 18: pin físico 12[cite: 7]
INDICADOR_PIN = 23 # BCM 23: pin físico 16[cite: 7]

# Inicialización de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(INDICADOR_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50) # PWM a 50 Hz[cite: 8]
pwm.start(0)

# Direcciones URL
url_servo = input("http://192.168.4.126:8080")
url_indicador = input("http://192.168.4.206:8080")

def obtener_datos(base_url, parametros):
    try:
        # Timeout para detección de fallas
        respuesta = requests.get(base_url + "/get?" + parametros, timeout=2) #[cite: 5]
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos
    except Exception as error:
        return None

def calcular_pwm(angulo):
    # Relación entre pulso y ciclo de trabajo[cite: 8, 9]
    # Rango típico: 1ms (0°) a 2ms (180°) -> Duty Cycle 5% a 10%
    duty = 5.0 + (angulo / 180.0) * 5.0
    return duty

tiempo_ultima_lectura_servo = time.monotonic()
tiempo_ultima_lectura_indicador = time.monotonic()

try:
    print("Iniciando control. Presiona Ctrl+C para detener.")
    while True:
        tiempo_actual = time.monotonic()
        
        # 1. Control del Servomotor (Teléfono 1)
        datos_servo = obtener_datos(url_servo, "accX&accY&accZ")
        if datos_servo and "buffer" in datos_servo:
            try:
                ax = datos_servo["buffer"]["accX"]["buffer"][-1]
                ay = datos_servo["buffer"]["accY"]["buffer"][-1]
                az = datos_servo["buffer"]["accZ"]["buffer"][-1]
                
                # Estimar inclinación[cite: 9]
                theta = math.atan2(ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
                
                # Limitar a rango -45° a 45° y mapear a 45° a 135°[cite: 9]
                theta = max(-45, min(45, theta))
                phi = theta + 90
                
                pwm.ChangeDutyCycle(calcular_pwm(phi))
                tiempo_ultima_lectura_servo = tiempo_actual
            except (KeyError, IndexError):
                pass
                
        # 2. Control del Indicador (Teléfono 2)
        datos_ind = obtener_datos(url_indicador, "linX&linY&linZ") # asumiendo nombres por defecto, verificar con /config[cite: 4]
        if datos_ind and "buffer" in datos_ind:
            try:
                lx = datos_ind["buffer"]["linX"]["buffer"][-1]
                ly = datos_ind["buffer"]["linY"]["buffer"][-1]
                lz = datos_ind["buffer"]["linZ"]["buffer"][-1]
                
                # Calcular magnitud de aceleración lineal[cite: 9]
                a_lin = math.sqrt(lx**2 + ly**2 + lz**2)
                
                # Criterio de activación > 15 m/s^2[cite: 9]
                if a_lin > 15:
                    GPIO.output(INDICADOR_PIN, GPIO.HIGH)
                else:
                    GPIO.output(INDICADOR_PIN, GPIO.LOW)
                tiempo_ultima_lectura_indicador = tiempo_actual
            except (KeyError, IndexError):
                pass
                
        # 3. Detección de fallas ( Timeout > 2s )[cite: 10]
        if (tiempo_actual - tiempo_ultima_lectura_servo) > 2.0:
            print("Falla de comunicación con Teléfono 1 (Servo). Suspendiendo señal PWM.")
            pwm.ChangeDutyCycle(0) # Se deshabilita señal PWM como medida de seguridad[cite: 10]
            
        if (tiempo_actual - tiempo_ultima_lectura_indicador) > 2.0:
            print("Falla de comunicación con Teléfono 2 (Indicador). Apagando indicador.")
            GPIO.output(INDICADOR_PIN, GPIO.LOW) # Apagar indicador ante fallo[cite: 10]

        time.sleep(0.1) # Frecuencia de consulta programada[cite: 6]

except KeyboardInterrupt:
    print("Finalizando ejecución...")
finally:
    # Apagar el indicador, detener PWM y liberar los GPIO[cite: 10]
    GPIO.output(INDICADOR_PIN, GPIO.LOW)
    pwm.stop()
    GPIO.cleanup()
