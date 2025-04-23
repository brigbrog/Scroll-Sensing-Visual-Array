'''
Brian Brogan
CS453
2 April 2025
Coordinator for reading serial data from glove sensor, activating design frictions, and writing to data file. 
'''

import pandas as pd
import numpy as np
import time
from collections import deque
import serial
from gpiozero import OutputDevice
from flux_led import WifiLedBulb
from random import randint
from time import sleep
import pygame

'''
to find serial ports macOS:  ls /dev/tty.*

2.5 mins for each condition
'''

raspi_portpath = '/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_018D7EEE-if00-port0'
#mac_portpath = '/dev/tty.usbserial-018D7EEE'

baud = 9600

#window_size = 50
#onset_threshold = 10.0          # Threshold for detecting a spike
#signal_buffer = deque(maxlen=window_size)

#Example MM output: ONSET,225574,16.90,null

# save df
scroll_df = pd.DataFrame(columns=["timestamp", "sig_diff", 'tap', 'df', 'app'])

#serial deque
event_buffer = deque(maxlen=10)

# serial info
glove_ser = serial.Serial(raspi_portpath, baud)

# smart bulb info
bulb_ip = "172.20.10.6"
bulb = WifiLedBulb(bulb_ip)
bulb.update_state()

# vibro motor info
v_motor = OutputDevice(17)

#audio init
pygame.init()
pygame.mixer.init()
#pygame.mixer.music.load('/home/bgbrog26/Desktop/SMGS/boing.wav')

def rand_light(bulb):
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    bulb.setRgb(r, g, b)
    
def boing():
    pass
    
def vibrate(motor, t):
    motor.on()
    sleep(t)
    motor.off()

def freq_light(bulb, code):
    if code == "y":
        bulb.setRgb(255, 255, 0)
    elif code == "r":
        bulb.setRgb(255, 0, 0)
    else:
        bulb.setRgb(0, 255, 0)

def freq_vibrate(motor, code):
    if code == "y":
        t = 0.5
    elif code == "r":
        t = 1.0
    else:
        t = 0.1
    motor.on()
    sleep(t)
    motor.off()

def freq_audio(code):
    if code == "y":
        pygame.mixer.music.load('/home/bgbrog26/Desktop/SMGS/beep2.mp3')
    elif code == "r":
        pygame.mixer.music.load('/home/bgbrog26/Desktop/SMGS/beep3.mp3')
    else:
        pygame.mixer.music.load('/home/bgbrog26/Desktop/SMGS/beep1.mp3')
    pygame.mixer.music.play()
    

if __name__ == "__main__":
    #random.seed(42)
    save_name = ""
    save = ""
    app = ""
    mode = ""
    while True:
        save = input("Save run? (y/n): ").lower()
        if save in ["y", "n"]:
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
        #df = input("select design friction -> (vib, vis, aud, com): ").lower()
        
    while True:    
        app = input("select mode (short, long): ").lower()
        if app in ["short", "long"]:
            break
        else:
            print("Invalid input. Please select valid mode.")
        
    while True:    
        mode = input("select mode (vib, vis, aud, all, none): ").lower()
        if mode in ["vib", "vis", "aud", "all", "none"]:
            break
        else:
            print("Invalid input. Please select valid mode.")
            
try:
    while True:
        ser_read = glove_ser.readline().decode('ascii', errors='ignore').strip()
        if ser_read.startswith('ONSET'):
            
            _, timestamp, sig_diff, tap = ser_read.split(",")
            print(f"Spike detected at {float(timestamp):.2f} | Δ: {float(sig_diff):.2f} | tap: {int(tap)}")

            if tap == '1':
                event_buffer.append(float(timestamp))
            

            scroll_df.loc[len(scroll_df)] = [int(timestamp), float(sig_diff), int(tap), mode, app]
            
            if mode != "none":

                freq = "g"
                delta_s = 0
                if len(event_buffer) == 10:
                    delta_s = (max(event_buffer) - min(event_buffer)) / 1000.0
                    if delta_s < 10:
                        freq = "r"
                    elif delta_s < 30:
                        freq = "y"

                # reactive df friction
                if tap == "1":
                    if mode == "vis":
                        #rand_light(bulb)
                        freq_light(bulb, freq)
                    if mode == "vib":
                        #vibrate(v_motor, 0.5)
                        freq_vibrate(v_motor, freq)
                    if mode == "aud":
                        #playsound('/home/bgbrog26/Desktop/SMGS/boing.wav')
                        #pygame.mixer.music.play()
                        freq_audio(freq)
                    if mode == "all":
                        freq_light(bulb, freq)
                        freq_vibrate(v_motor, freq)
                        freq_audio(freq)
                        #pygame.mixer.music.play()
                print("timestamp delta: " + str(delta_s))

except KeyboardInterrupt:
    print("\nStopped by user. Final spike events:")
    if save == "y":
        save_name = input("enter filename to save run: ")
        #save the dataframe to json or csv or something
        scroll_df.to_csv("./output/"+save_name)

    else:
        print(f"{scroll_df.shape[0]} scrolls detected")
