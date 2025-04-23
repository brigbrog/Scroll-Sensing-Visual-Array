from gpiozero import OutputDevice
from time import sleep

motor = OutputDevice(17)

if __name__ == "__main__":
    motor.on()
    sleep(1)
    motor.off()
