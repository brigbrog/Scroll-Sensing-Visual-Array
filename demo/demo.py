import serial.tools.list_ports
import time
from flux_led import WifiLedBulb

## Brian Brogan - March 1, 2025
## This file holds the demo code for basic smart LED serial dimmer ciruit.
#(port = '/dev/cu.usbserial-018D7EEE')
ports = serial.tools.list_ports.comports()
controller = serial.Serial()
brightness = 0.0
portsList = []

bulb_ip = "172.20.10.6"
bulb = WifiLedBulb(bulb_ip)
bulb.update_state()  # Retrieve the current state

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

controller.baudrate = 9600
controller.port = "/dev/cu.usbserial-018D7EEE"
controller.open()

while True:
    #time.sleep(1)
    if controller.in_waiting:
        packet = controller.readline()
        brightness = float(packet.decode('utf').strip())
        print(brightness)
    if brightness < 341:
        bulb.setRgb(255, 0, 0)
    if brightness > 341 and brightness < 680:
        bulb.setRgb(0, 255, 0)
    if brightness >= 680:
        bulb.setRgb(0, 0, 255)