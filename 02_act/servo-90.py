import time
import RPi.GPIO as GPIO

# Configuración del pin
SERVO = 18  # BCM 18 (Pin físico 12)

# Configuración de la librería GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO, GPIO.OUT)

# Iniciar PWM a 50Hz
pwm = GPIO.PWM(SERVO, 50)

try:
    # 7.5 es el duty cycle para 90 grados (posición central)
    pwm.start(7.5)
    
    # Le damos 1 segundo al servo para que llegue a la posición
    time.sleep(1)
    
finally:
    # Detener PWM y limpiar los pines GPIO
    pwm.stop()
    GPIO.cleanup()
