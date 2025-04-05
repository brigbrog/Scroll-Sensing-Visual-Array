'''
Brian Brogan
CS453
2 April 2025
Test File for reading serial data from glove sensor /  and writing to data file. 
'''

import pandas as pd
import numpy as np
import time
from collections import deque
import serial

'''
to find serial ports macOS:  ls /dev/tty.*
'''

#raspi_portpath = '/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_018D7EEE-if00-port0'
mac_portpath = '/dev/tty.usbserial-018D7EEE'
baud = 9600
#window_size = 50
#onset_threshold = 10.0          # Threshold for detecting a spike
#signal_buffer = deque(maxlen=window_size)

#ONSET,225574,16.90,null

scroll_df = pd.DataFrame(columns=["timestamp", "sig_diff", 'tap'])

glove_ser = serial.Serial(mac_portpath, baud)

save_name = ""
save = ""

if __name__ == "__main__":
    while True:
        save = input("Save run? (y/n): ").lower()
        if save in ["y", "n"]:
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
try:
    while True:
        ser_read = glove_ser.readline().decode('ascii', errors='ignore').strip()

        if ser_read.startswith('ONSET'):
            _, timestamp, sig_diff, tap = ser_read.split(",")
            print(f"Spike detected at {float(timestamp):.2f} | Δ: {float(sig_diff):.2f} | tap: {int(tap)}")
            scroll_df.loc[len(scroll_df)] = [int(timestamp), float(sig_diff), int(tap)]
        time.sleep(0.05)  # Simulate real-time delay (20 Hz sampling rate)

except KeyboardInterrupt:
    print("\nStopped by user. Final spike events:")
    if save == "y":
        save_name = input("enter filename to save run: ")
        #save the dataframe to json or csv or something
        scroll_df.to_csv("./output/"+save_name)

    else:
        print(f"{scroll_df.shape[0]} scrolls detected")