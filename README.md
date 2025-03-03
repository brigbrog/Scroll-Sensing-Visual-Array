# Smart Bulb Dimmer Circuit

## Overview
This project is an Arduino circuit with a smart light bulb using serial communication and Wi-Fi control. The system adjusts the color of the smart bulb based on the brightness level read from an analog sensor.

## Components
- Arduino 
- Potentiometer (10k)
- USB/USB-C Serial Connection
- Flux WiFi Smart Bulb (with the `flux_led` library)

## How It Works
1. The Arduino reads analog brightness values from the sensor (0-1023) and transmits them via serial communication.
2. A Python script reads the serial data, converts the brightness value, and sends Wi-Fi commands to the Flux bulb.
3. The bulb displays different colors based on brightness thresholds:
   - Red for low brightness (0-340)
   - Green for medium brightness (341-679)
   - Blue for high brightness (680-1023)

## Prerequisites
### Hardware
- Metro Mini
- Breadboard

### Software
- Python 3.x
- `flux_led` library
- `pyserial` library

Install required libraries:
```bash
pip install flux_led pyserial
python bulb_script.py
```

## Setup

1. Connect the analog sensor to the Arduino's A0 pin.
2. Upload the following code to the Arduino:

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  float cur = analogRead(A0);
  Serial.println(cur);
  delay(100);
}
```

3. Connect the Arduino to your computer via USB/USB-C.
4. Update the bulb_ip in the Python script to match your smart bulb's IP address.
5. Update the serial port name in the Python script to match your device's port.
6. Run the Python script:

```bash
python bulb_script.py
```

## Acknowledgments

- flux_led library: https://github.com/Danielhiversen/flux_led
- pyserial library: https://pyserial.readthedocs.io/
