#include "MyFilter.h"

const int stretchPin = A0;
const int tapPin = A1;

const int windowSize = 10;
float window[windowSize];
MovingAverage stretchAvg(window, windowSize);
//MovingAverage tapAvg(window, windowSize);

// stretch detection sensitivity
const float stretchFactor = 15.0; 

// tap detection sensitivity
const float tapFactor = 10.0;

//dedounce
float lastOnsetTime = 0;
unsigned long debounceTime = 500; // ms between allowed onsets

void setup() {
  Serial.begin(9600);
}

void loop() {
  float stretch_sig = analogRead(stretchPin);
  float tap_sig = analogRead(tapPin);
  float stretch_smooth = stretchAvg.update(stretch_sig);
  //float tap_smooth = tapAvg.update(tap_sig); 

  float stretch_diff = abs(stretch_sig - stretch_smooth);
  //float tap_diff = abs(tap_sig - tap_smooth);
  unsigned long currentTime = millis();

  //Serial.print(stretch_sig);  // Print the first value
  //Serial.print(" ");      // Add a space as a delimiter
  //Serial.print(smoothed);  // Print the second value
  //Serial.println();

  // Detect sudden onset (spike) with tap thing
  if (stretch_diff > stretchFactor && (currentTime - lastOnsetTime > debounceTime)) {
    Serial.print("ONSET,");
    Serial.print(currentTime);
    Serial.print(",");
    Serial.print(stretch_diff);
    if (tap_sig > tapFactor){
      Serial.print(",");
      Serial.println("1");
    }
    else {
      Serial.print(",");
      Serial.println("0");
    }
    lastOnsetTime = currentTime;
  }

  delay(25); // Adjust based on your sampling needs
}


