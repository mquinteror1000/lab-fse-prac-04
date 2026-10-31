import RPi.GPIO as GPIO
import time

BUZZER_PIN = 23

# Configuración del pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def beep(repeticiones, duracion_encendido, duracion_apagado):
    for _ in range(repeticiones):
        GPIO.output(BUZZER_PIN, GPIO.HIGH) # Enciende el buzzer
        time.sleep(duracion_encendido)     # Espera con el sonido encendido
        
        GPIO.output(BUZZER_PIN, GPIO.LOW)  # Apaga el buzzer
        time.sleep(duracion_apagado)       # Espera en silencio

try:
    print("Iniciando alarma...")
    # Pitar 3 veces: 0.2 segundos encendido, 0.2 segundos apagado
    beep(3, 0.2, 0.2)
    print("Alarma finalizada.")

except KeyboardInterrupt:
    print("\nDetenido por el usuario.")

finally:
    # Apagamos por seguridad y limpiamos
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.cleanup()
