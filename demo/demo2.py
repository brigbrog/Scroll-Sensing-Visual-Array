import serial
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



mm_portpath = '/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_018D7EEE-if00-port0'
baud = 9600
window_size = 50

glove_ser = serial.Serial(mm_portpath,
						  baud)
#glove_ser.flushInput()

#plt.ion()
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2)
ax.set_xlim(0.0, 100.0)
ax.set_ylim(50.0, 200.0)
ax.set_xlabel('Time (cycles)')
ax.set_ylabel('Glove Action')

def update(frame):
	if glove_ser.in_waiting > 0:
		reading = glove_ser.readline().decode('ascii', errors='ignore').strip()
		#print(data)
		#try:
		fl_reading = float(reading)
		
		x_data.append(len(x_data))
		y_data.append(fl_reading)
		
		#if len(x_data) > window_size:
			#x_data.pop(0)
			#y_data.pop(0)
			
		ax.set_xlim(max(0, len(x_data) - 30), len(x_data))
		ax.set_ylim(fl_reading-100, fl_reading+100)
			
		line.set_data(x_data, y_data)
		#print(reading, flush = True)
		
		return line
		#except ValueError:
			#pass
	#return line
	
ani = FuncAnimation(fig,
					update,
					frames = window_size,
					#blit = False,
					interval = 25)


plt.show()

