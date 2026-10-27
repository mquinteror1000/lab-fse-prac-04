import time
import RPi.GPIO as GPIO

SERVO = 18  # BCM 18 (Pin físico 12)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO, GPIO.OUT)

pwm = GPIO.PWM(SERVO, 50)

try:
    # 12.5 es el duty cycle para 180 grados
    pwm.start(12.5)
    time.sleep(1)
    
finally:
    pwm.stop()
    GPIO.cleanup()
