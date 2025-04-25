'''
Brian Brogan
CS453
2 April 2025
Coordinator for reading serial data from glove sensor, activating design frictions, and writing to data file. 
'''

import pandas as pd
from collections import deque
import serial
from gpiozero import OutputDevice
from flux_led import WifiLedBulb
from random import shuffle
from time import sleep, time
import pygame
import os

'''
to find serial ports macOS:  ls /dev/tty.*

2.5 mins for each condition -> dur = 150

Example MM output: ONSET,225574,16.90,null
'''

#Port Path for Raspi/MetroMini Serial connection
raspi_portpath = '/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_018D7EEE-if00-port0'

# save df
scroll_df = pd.DataFrame(columns=["run", "participant", "timestamp", "scroll delta", 'tap', 'design friction', 'content type'])

# serial info
baud = 9600
glove_ser = serial.Serial(raspi_portpath, baud)

# smart bulb info
bulb_ip = "172.20.10.6"
bulb = WifiLedBulb(bulb_ip)
bulb.update_state()

# vibro motor info
v_motor = OutputDevice(17)

def get_freq(buffer):
    
    freq = "g"
    delta_ts = 25
        
    if len(buffer) == 10:
        delta_ts = (max(buffer) - min(buffer)) / 1000.0
        if delta_ts < 15:
            freq = "r"
        elif delta_ts < 25:
            freq = "y"
    return delta_ts, freq

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


def participant_op(base_dir,
                   dur,
                   ID,
                   save_df: pd.DataFrame,
                   save
                   #cont_type
                   ):
    #ID = run(2)+part(2)
    #dur = 150 -> 2.5 mins
    print(f"Starting Run with ID: {ID}")
    run_code = ID[:2]
    part_code = ID[2:]
    save_path = f"{base_dir}"

    cont_type = input("Specify content type for new participant: (short/long)").lower().strip()

    # randomly order design frictions with calibration always first
    seq = ["cal"]
    fric_list = ["all", "vis", "vib", "aud"]
    shuffle(fric_list)
    seq.extend(fric_list)

    print(f"Running participant {part_code} with sequence {seq}")

    

    for i, des_fric in enumerate(seq):
        event_buffer = deque(maxlen=10)
        print("Beginning " + des_fric + " mode.")
        start_time = time()
        while time() - start_time < dur:
            ser_read = glove_ser.readline().decode('ascii', errors='ignore').strip()
            if ser_read.startswith('ONSET'):
                _, timestamp, sig_diff, tap = ser_read.split(",")
                print(f"Spike at {float(timestamp):.2f} | Δ: {float(sig_diff):.2f} | tap: {int(tap)}")

                #if tap == '1': --> TAP OPTION
                event_buffer.append(float(timestamp))

                if des_fric != "cal":
                    delta_ts, freq = get_freq(event_buffer)
                    # visual
                    if des_fric == "vis":
                        freq_light(bulb, freq)
                    # vibration
                    elif des_fric == "vib":
                        freq_vibrate(v_motor, freq)
                    # audio
                    elif des_fric == "aud":
                        freq_audio(freq)
                    # all
                    elif des_fric == "all":
                        freq_light(bulb, freq)
                        freq_vibrate(v_motor, freq)
                        freq_audio(freq)
                    # print delta timestamp from event buffer
                    print(f"TS Δ: {delta_ts}, FREQ: {freq}")
                
                save_df.loc[len(save_df)] = [run_code, part_code,
                                                 int(timestamp),
                                                 float(sig_diff),
                                                 int(tap),
                                                 des_fric,
                                                 cont_type]
            
    print(f"Testing for participant {part_code} complete.")

    run_again = input("Create new participant in this run? (y/n)").lower().strip()
    if run_again == "y":
        new_part_code = str(int(ID[3]) + 1) if int(ID[3]) + 1 > 10 else '0' + str(int(ID[3]) + 1)
        new_ID = ID[:2] + new_part_code
        participant_op(base_dir, 
                       dur, 
                       new_ID, 
                       save_df,
                       save
                       )
    elif run_again == "n":
        if save == "y":
            fname = f"/{ID[:2]}.csv"
            fpath = save_path + fname
            save_df.to_csv(fpath)
            print(f"Saving results to {save_path}")
        elif save == "n":
            print(f"{len(scroll_df[scroll_df['participant'] == part_code])} scrolls detected for participant {part_code}.")

    return save_df
                

if __name__ == "__main__":

    #ID = run(2)+part(2)

    #pygame audio init
    pygame.init()
    pygame.mixer.init()

    save_run = input("Save Run? (y/n)").lower().strip()
    
    out_dir = './output'
    os.makedirs(out_dir, exist_ok=True)
    out_dir_len = len(os.listdir(out_dir))
    
    run_code = str(out_dir_len) if out_dir_len > 10 else '0' + str(out_dir_len)
    
    ID_init = run_code + '00'
    
    scroll_df = participant_op(out_dir,
                                2,
                                ID_init,
                                scroll_df,
                                save_run)
    
    print(f"Saved data shape: {scroll_df.shape}")
    print(scroll_df.head())


