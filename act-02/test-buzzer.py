import RPi.GPIO as GPIO
import time

# Pin GPIO donde conectaste la pata larga (+)
BUZZER_PIN = 23

# Configuración inicial
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    print("Prueba 1: Probando como Buzzer ACTIVO (Señal continua)...")
    # Un buzzer activo sonará fuerte y claro aquí. 
    # Un buzzer pasivo solo hará un pequeño "clic" o ruido muy bajo.
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(2)
    
    # Apagamos y hacemos una pausa
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(1)

    print("Prueba 2: Probando como Buzzer PASIVO (Señal PWM a 1000Hz)...")
    # Un buzzer pasivo necesita frecuencia para sonar y aquí generará un tono claro.
    # Un buzzer activo aquí podría sonar distorsionado o exactamente igual que en la Prueba 1.
    pwm = GPIO.PWM(BUZZER_PIN, 1000) # Frecuencia de 1000 Hz
    pwm.start(50)                    # Duty cycle del 50%
    time.sleep(2)
    
    pwm.stop()

except KeyboardInterrupt:
    print("\nPrueba interrumpida por el usuario.")

finally:
    # Limpiamos los pines para evitar advertencias en futuras ejecuciones
    GPIO.cleanup()
    print("Pines liberados. Fin de la prueba.")
