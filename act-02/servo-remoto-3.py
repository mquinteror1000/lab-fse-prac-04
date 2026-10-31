import math
import time
import requests
import RPi.GPIO as GPIO

SERVO_PIN = 18
BUZZER_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

url_servo = "http://192.168.4.126:8080"
url_indicador = "http://192.168.4.126:8080"
TIMEOUT_PETICION = 20.0 

def beep(repeticiones, duracion_encendido, duracion_apagado):
    for _ in range(repeticiones):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duracion_encendido)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(duracion_apagado)

def obtener_datos(base_url, parametros):
    try:
        respuesta = requests.get(base_url + "/get?" + parametros, timeout=TIMEOUT_PETICION) 
        respuesta.raise_for_status()
        return respuesta.json()
    except Exception:
        return None

def calcular_pwm(angulo):
    duty = 2.5 + (angulo / 180.0) * 10.0
    return duty

tiempo_ultima_lectura_servo = time.monotonic()
tiempo_ultima_lectura_indicador = time.monotonic()

try:
    print("Iniciando control remoto con alarma. Presiona Ctrl+C para detener.")
    while True:
        datos_servo = obtener_datos(url_servo, "accX&accY&accZ")
        if datos_servo and "buffer" in datos_servo:
            try:
                ax = datos_servo["buffer"]["accX"]["buffer"][-1]
                ay = datos_servo["buffer"]["accY"]["buffer"][-1]
                az = datos_servo["buffer"]["accZ"]["buffer"][-1]
                
                theta = math.atan2(ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
                theta = max(-45, min(45, theta))
                phi = theta + 90
                
                pwm.ChangeDutyCycle(calcular_pwm(phi))
                tiempo_ultima_lectura_servo = time.monotonic()
            except (KeyError, IndexError):
                pass
                
        datos_ind = obtener_datos(url_indicador, "linX&linY&linZ")
        if datos_ind and "buffer" in datos_ind:
            try:
                lx = datos_ind["buffer"]["linX"]["buffer"][-1]
                ly = datos_ind["buffer"]["linY"]["buffer"][-1]
                lz = datos_ind["buffer"]["linZ"]["buffer"][-1]
                
                a_lin = math.sqrt(lx**2 + ly**2 + lz**2)
                
                if a_lin > 1:
                    beep(1, 0.2, 0.05)
                else:
                    GPIO.output(BUZZER_PIN, GPIO.LOW)
                tiempo_ultima_lectura_indicador = time.monotonic()
            except (KeyError, IndexError):
                pass
                
        if (time.monotonic() - tiempo_ultima_lectura_servo) > (TIMEOUT_PETICION + 2.0):
            pwm.ChangeDutyCycle(0) 
            
        if (time.monotonic() - tiempo_ultima_lectura_indicador) > (TIMEOUT_PETICION + 2.0):
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(0.1) 

except KeyboardInterrupt:
    print("\nFinalizando ejecución...")
finally:
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    pwm.stop()
    GPIO.cleanup()
